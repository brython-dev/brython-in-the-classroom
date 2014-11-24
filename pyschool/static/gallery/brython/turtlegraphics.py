import turtle
t=turtle.Turtle()

t.penup()
t.left(45)
t.backward(125)
t.right(45)
t.pendown()

for c in ['red', 'green', 'yellow', 'blue']:
    t.color(c)
    t.forward(75)
    t.left(90)

t1=turtle.Turtle("turtle")
t1.penup()

t1.pendown()
t1.width(3)
for c in ['red', 'blue', 'yellow', 'green', 'purple', 'brown']:
    t1.color(c)
    t1.forward(50)
    t1.left(60)

t1.penup()
t1.left(60)
t1.backward(120)

t1.pendown()
t1.color('red')
t1.write("I love Brython!!")

turtle._Screen().end()
