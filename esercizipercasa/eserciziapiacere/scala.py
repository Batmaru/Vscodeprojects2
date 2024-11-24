import turtle


larghezza = 400  
altezza = 200    
num_scalini = 9  


larghezza_scalino = larghezza // num_scalini
altezza_scalino = altezza // num_scalini


turtle.setup(width=600, height=400)
turtle.speed(9)  

def disegna_scala():
    
    turtle.penup()
    turtle.goto(-larghezza // 2, altezza // 2)
    turtle.pendown()
    
    
    for _ in range(2):
        turtle.forward(larghezza)
        turtle.right(90)
        turtle.forward(altezza)
        turtle.right(90)
    
  
    turtle.penup()
    turtle.goto(-larghezza // 2, altezza // 2 - altezza_scalino)
    turtle.pendown()

    # Disegna la scala
    for i in range(num_scalini - 1):
        turtle.forward(larghezza_scalino)  
        turtle.right(90)
        turtle.forward(altezza_scalino)    
        turtle.left(90)


disegna_scala()


turtle.done()