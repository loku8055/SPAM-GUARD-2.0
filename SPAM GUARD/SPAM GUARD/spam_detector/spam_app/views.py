import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# Fulfilling the exact requirement alias
from .models import Prediction as SpamPrediction
from .predictor import predict


def get_prediction(text_message):
    """
    Helper Function: Takes a text message, vectorizes it, predicts if it is spam,
    calculates the confidence score, saves the result to SpamPrediction,
    and returns the is_spam boolean and confidence score.
    """
    result = predict(text_message)
    is_spam = result['label'] == 'spam'
    confidence = result['confidence']
    
    prediction_obj = SpamPrediction.objects.create(
        text=text_message,
        result=result['label'],
        confidence=confidence,
        spam_probability=result['spam_probability'],
        ham_probability=result['ham_probability']
    )
    
    return is_spam, confidence, prediction_obj


def home(request):
    """Home page."""
    if request.user.is_authenticated:
        recent = SpamPrediction.objects.filter(user=request.user).order_by('-created_at')[:10]
        stats = {
            'total': SpamPrediction.objects.filter(user=request.user).count(),
            'spam_count': SpamPrediction.objects.filter(user=request.user, result='spam').count(),
            'ham_count': SpamPrediction.objects.filter(user=request.user, result='ham').count(),
        }
    else:
        recent = list(SpamPrediction.objects.all().order_by('-created_at')[:10])
        # Clear text for global privacy and set flag for UI
        for p in recent:
            p.text = ""
            p.is_hidden_for_privacy = True
            
        stats = {
            'total': SpamPrediction.objects.count(),
            'spam_count': SpamPrediction.objects.filter(result='spam').count(),
            'ham_count': SpamPrediction.objects.filter(result='ham').count(),
        }

    if stats['total'] > 0:
        stats['spam_pct'] = round(stats['spam_count'] / stats['total'] * 100, 1)
        stats['ham_pct'] = round(stats['ham_count'] / stats['total'] * 100, 1)
    else:
        stats['spam_pct'] = 0
        stats['ham_pct'] = 0

    return render(request, 'spam_app/Home.html', {
        'recent_predictions': recent,
        'stats': stats,
    })


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'spam_app/Register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'spam_app/Login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    logout(request)
    return redirect('home')


@login_required
def predict_view(request):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if not text:
            return render(request, 'spam_app/Predict.html', {'error': 'No text provided.'})
            
        is_spam, confidence, prediction_obj = get_prediction(text)
        
        # Link to current user
        prediction_obj.user = request.user
        prediction_obj.save()
        
        return redirect('result', prediction_id=prediction_obj.id)
        
    return render(request, 'spam_app/Predict.html')


@login_required
def result_view(request, prediction_id):
    prediction = get_object_or_404(SpamPrediction, id=prediction_id, user=request.user)
    return render(request, 'spam_app/Result.html', {'prediction': prediction})


@csrf_exempt
def api_detect_spam(request):
    """Extension API View"""
    if request.method == 'OPTIONS':
        response = JsonResponse({'status': 'ok'})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            if not message:
                return JsonResponse({'status': 'error', 'message': 'No message provided'}, status=400)
                
            is_spam, confidence, _ = get_prediction(message)
            response = JsonResponse({
                'status': 'success',
                'is_spam': is_spam,
                'confidence': confidence
            })
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type"
            return response
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed. Use POST or OPTIONS.'}, status=405)


def antigravity_view(request):
    """Easter Egg View"""
    return redirect('https://xkcd.com/353/')


@csrf_exempt
@require_POST
def classify(request):
    """Original legacy API endpoint"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
    except (json.JSONDecodeError, AttributeError):
        text = request.POST.get('text', '').strip()

    if not text:
        return JsonResponse({'error': 'No text provided.'}, status=400)

    if len(text) < 5:
        return JsonResponse({'error': 'Text too short to classify.'}, status=400)

    is_spam, confidence, prediction_obj = get_prediction(text)
    
    if request.user.is_authenticated:
        prediction_obj.user = request.user
        prediction_obj.save()

    response = JsonResponse({
        'id': prediction_obj.id,
        'label': prediction_obj.result,
        'confidence': prediction_obj.confidence,
        'spam_probability': prediction_obj.spam_probability,
        'ham_probability': prediction_obj.ham_probability,
        'confidence_level': prediction_obj.confidence_level,
        'created_at': prediction_obj.created_at.strftime('%b %d, %Y %H:%M'),
    })
    response["Access-Control-Allow-Origin"] = "*"
    return response


def history(request):
    """Returns all stored predictions as JSON."""
    if request.user.is_authenticated:
        predictions = SpamPrediction.objects.filter(user=request.user)[:50]
    else:
        predictions = SpamPrediction.objects.all()[:50]
        
    data = []
    for p in predictions:
        text_preview = p.text[:80] + '...' if len(p.text) > 80 else p.text
        if not request.user.is_authenticated:
            text_preview = "[ ENCRYPTED TEXT ]"
            
        data.append({
            'id': p.id,
            'text': text_preview,
            'result': p.result,
            'confidence': p.confidence,
            'confidence_level': p.confidence_level,
            'created_at': p.created_at.strftime('%b %d, %Y %H:%M'),
        })
        
    return JsonResponse({'predictions': data})
