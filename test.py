import keyboard

class Node:
    def __init__ (self, text):
        self.text = text
        self.prev = None
        self.next = None

#Quando for executar o programa, deve haver um arquivo com a nomeclatura "teste.txt" na mesma pasta
#o programa se encontra, assim, insira algum texto para poder editá-lo, dessa forma você poderá
#executar o programa "python test.py" e aparecerá o menu contendo as informações que pode fazer no programa

class TextEditor:

    def __init__(self):
        self.head = self.cursor = Node("")
        self.leftLen = 0
        self.totale = 0

    def addText(self, text: str) -> None:
        newNode = Node(text)
        
        nxt = self.cursor.next
        self.cursor.next = newNode
        
        newNode.prev = self.cursor
        newNode.next = nxt
        if nxt:
            nxt.prev = newNode
        
        self.cursor = newNode
        self.leftLen += (len(text))-1
        self.totale += (len(text))
        print(self.cursor.text)
    
    
    def last10(self):
        if self.leftLen == 0:
            return ""
        
        k = min(1000, self.leftLen)
        res = "" 
        cur = self.cursor
        
        while cur != self.head and k >= len(cur.text):
            k -= len(cur.text)
            res = cur.text + res
            cur = cur.prev   
        if k > 0:   
            td = len(cur.text) - k  
            rem = cur.text[td:]
            res = rem + res
        return res

    def deleteText(self, k: int) -> int:
       
        ll = self.leftLen
        
        if self.leftLen == 0:
            return 0

        while self.cursor != self.head and k >= len(self.cursor.text):
            nxt = self.cursor.next
            prv = self.cursor.prev
            prv.next = nxt
            
            if nxt:
                nxt.prev = prv
            
            k -= len(self.cursor.text)
            self.leftLen -= len(self.cursor.text)
            
            self.cursor = prv

        if k > 0:
            if self.leftLen == 0:
                return ll
            
            td = len(self.cursor.text) - k
            self.cursor.text = self.cursor.text[:td]
            
            self.leftLen -= k
            
        return ll - self.totale

    def cursorLeft(self, k: int) -> str:
        if self.leftLen == 0:
            return ""
        
        cur = self.cursor
        
        while cur != self.head and k >= len(cur.text):
            k -= len(cur.text)
            self.leftLen -= len(cur.text)
            cur = cur.prev
            
        self.cursor = cur
        
        if k > 0:
            if self.leftLen == 0:
                return ""
            
            td = len(self.cursor.text) - k
            rem = self.cursor.text[td:]
            self.cursor.text = self.cursor.text[:td]
            self.leftLen -= k
            
            temp, tln = self.cursor, self.leftLen
            self.addText(rem)
            self.cursor = temp
            self.leftLen = tln
            
        return self.leftLen 

    def cursorRight(self, k: int) -> str:    
        cur = self.cursor
        nxt = self.cursor.next
        
        while nxt and k >= len(nxt.text):
            k -= len(nxt.text)
            self.leftLen += len(nxt.text)
            cur = nxt
            nxt = nxt.next
            
        self.cursor = cur
            
        if k > 0:
            if not cur.next:
                return self.last10()
            
            cur = cur.next
            
            rem = cur.text[k:]
            cur.text = cur.text[:k]
            
            self.leftLen += k
            self.cursor = cur
            
            temp, tln = self.cursor, self.leftLen
            
            self.addText(rem)
            self.cursor = temp
            self.leftLen = tln
        
        return self.last10()
    
    def total(self):
        if self.total == 0:
            return ""
        
        k = min(1000, self.totale)
        res = ""
        cur = self.cursor
        
        while cur != self.head and k >= len(cur.text):
            k -= len(cur.text)
            res = cur.text + res
            cur = cur.prev  
        if k > 0: 
            td = len(cur.text) - k    
            rem = cur.text[td:]
            res = rem + res
        return res
                    
bloco = TextEditor()
with open("teste.txt", "r", encoding="utf-8") as arquivo:
    txt = arquivo.read()   
bloco.addText(txt)

def save():
    with open("teste.txt", "w") as arquivo:
        if bloco.cursor.next is None:
            recebe = bloco.total()
        else:
            recebe = bloco.total() + bloco.cursor.next.text
        arquivo.write(recebe)

def escrever():
    texto = input("escreva o texto: ")
    bloco.addText(texto)
    save()

def bloco_esquerda():
    bloco.cursorLeft(1)
    if len(bloco.cursor.text)<2:
        print(bloco.cursor.text)
        save()

def bloco_direita():
    bloco.cursorRight(1)
    if len(bloco.cursor.text)<2:
        print(bloco.cursor.text)
        save()

def deletar():
    bloco.deleteText(1)
    print("um caracter foi deletado")
    save()

print("funções: " , "\n", "+ = escrever", "\n", "seta esquerda = cursor pra esquerda", 
        "\n", "seta direita = cursor pra direita", "\n", "delete = deletar caracter anterior ao cursor")

keyboard.add_hotkey("+", escrever)
keyboard.add_hotkey("left arrow", bloco_esquerda)
keyboard.add_hotkey("right arrow", bloco_direita)
keyboard.add_hotkey("delete", deletar)
keyboard.wait('esc')