from django.shortcuts import render
import logica_negocio.snake_game as sg

# Create your views here.

def snake_game_view(request):
    game = {'Display': sg.Display(),
            'Score': sg.Score(),
            'Snake': sg.Snake(),
            'Food': sg.Food()}
    return render(request, 'snake/game.html', {'game': game})