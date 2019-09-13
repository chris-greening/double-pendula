<h1>Double Pendula</h1>

Double pendula simulation written in Python. The program uses Lagrangian mechanics to showcase the chaotic movements in slightly offset double pendula (essentially the Butterfly Effect).

This is a really informal prototype, I'm looking to expand this in the future when I have time. Going to add in some data analysis, graphs, gifs, etc<

Changing the pendulum to observe different effects is not very hard, just change this statement:

```python
    for _ in range(10):
        pendula.append(DoublePendulum(L1=L1,L2=L2,y0=[initial_theta-initial_dtheta, 0,0,0], color=random_hex()))
        initial_dtheta += dtheta
```

The range indicates how many pendula are created and the arguments passed to DoublePendulum indicate length of arm one, length of arm two, etc etc. Like I said, I plan on really fleshing this out further but this is just a prototype with really garbage documentation (if you have questions, just ask!)