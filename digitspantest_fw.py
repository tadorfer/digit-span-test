
import tkinter as tk     
import random


docs = '''\nThis is a Digit Span Test that evaluates working memory performance.
Try to remember the digits in the order that they are presented and repeat
them once the sequence has stopped. If successful, the length of the 
sequence will increase by 1. You can enter three incorrect sequences before the 
test gets terminated. We will start out with 3 digits.
\nClick 'Start' or press 'Enter' if you are ready to start the test.'''

title = 'Digit Span Test for Working Memory Evaluation'


def startTest(*args):
    nums = ['Three','Four','Five','Six','Seven','Eight', 'Nine','Ten','Eleven',
            'Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen']
    wdw.unbind('<Return>')
    canvas.delete('all')
    while True:
        global i, DIGITS
        DIGITS += 1
        i += 1
        counter = i-1
        txt = '{0}-Digit Sequence'.format(nums[i-1])
        seqtxt = canvas.create_text(Width/2, Height/3.5, fill='darkblue', 
                                                         font='Arial 32', 
                                                         text=txt, 
                                                         justify='c')
        canvas.after(1200, canvas.update())
        seq = random.sample(range(10), DIGITS)
        while consecutive(seq) == False:
            seq = random.sample(range(10), DIGITS)
      
        seq = str(seq)
        seq_digits = ''.join(c for c in seq if c.isdigit())
        length = len(seq_digits)
        for a in range(length):
            z = canvas.create_text(Width/2, Height/2, fill='darkblue', 
                                                      font='Times 160', 
                                                      text=seq_digits[a], 
                                                      justify='c')
            canvas.after(1000,canvas.update())
            canvas.delete(z)        
        
        label = canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                                        font='Arial 26', 
                                                        text='Repeat the sequence here', 
                                                        justify='c')
        
        entry = tk.Text(wdw, width=length, height=1, font=('Arial', 32))
        e = canvas.create_window(Width/2, Height/2, window=entry)
        entry.focus()
        
        def delete():
            canvas.delete('all')
            startTest()
            
        def get_text(event=None):
            global userNumbers, generatedNumbers, FAILURES
            content = entry.get(1.0, "end-1c")
            userNumbers.append(content)
            generatedNumbers.append(seq_digits)
            canvas.delete(label, b, e, seqtxt)
            if content == seq_digits:
                canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                                        font='Arial 26', 
                                                        text='Correct! Continue...', 
                                                        justify='c')
                canvas.after(1200, delete)
            else:
                canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                                        font='Arial 26', 
                                                        text='Try again!', 
                                                        justify='c')
                FAILURES += 1
                if FAILURES < 3:
                    global i, DIGITS
                    i -= 1
                    DIGITS -= 1
                    canvas.after(1200, delete)
                else:
                    canvas.delete('all')
                    canvas.create_text(Width/2, Height/2.3, fill='darkblue', 
                                                            font='Arial 26', 
                                                            text='Thank you for your participation!', 
                                                            justify='c')

                    canvas.create_text(Width/2, Height/2, fill='darkblue', 
                                                          font='Arial 36', 
                                                          text='Your score: {0}'.format(counter), 
                                                          justify='c')

                    wdw.after(3000, lambda: wdw.destroy())
                
        button2 = tk.Button(wdw, height=2, width=10, text='Continue', 
                                                     font='Arial 20', 
                                                     fg='black', 
                                                     command=get_text, bd=0)
        button2.configure(bg='#4682B4', 
                          activebackground='#36648B', 
                          activeforeground='white')
        entry.bind('<Return>', get_text)  
        b = canvas.create_window(Width/2, Height/1.6, window=button2)
        break
    

def consecutive(sequence):
    l = len(sequence)
    res = []
    for x in range(l-1):
        if sequence[x] == sequence[x+1]+1 or sequence[x] == sequence[x+1]-1:
            res.append(1)
    if len(res) > 0:
        return False


wdw = tk.Tk()
wdw.title('Digit Span Test')
Width = wdw.winfo_screenwidth()
Height = wdw.winfo_screenheight()
wdw.geometry("%dx%d" % (Width, Height))
canvas = tk.Canvas(wdw, bg='#FDF5E6')
canvas.pack(fill = 'both', expand = True)
wdw.state('zoomed')

canvas.create_text(Width/2, Height/4.5, fill='darkblue', 
                                        font='Arial 52', 
                                        text=title, 
                                        justify='c')

canvas.create_text(Width/2, Height/2.2, fill='darkblue', 
                                        font='Arial 36', 
                                        text=docs, 
                                        justify='c')

i = 0
DIGITS = 2
FAILURES = 0

wdw.bind('<Return>', lambda event: startTest())
userNumbers, generatedNumbers = [], []

button1 = tk.Button(wdw, height=2, width=8, text='Start', 
                                            font='Arial 24', 
                                            fg='black', 
                                            command=startTest, 
                                            bd=0)

button1.configure(bg='#4682B4', 
                  activebackground='#36648B', 
                  activeforeground='white')
                  
canvas.create_window(Width/2, Height/1.4, window=button1)

wdw.mainloop()

print('Generated: ', generatedNumbers)
print('Repeated:  ', userNumbers)