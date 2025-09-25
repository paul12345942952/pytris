import pygame
import random

class InputHandler:
    def __init__(self):
        self.left=False
        self.right=False
        self.down=False

        self.rotate=False
        
        self.pause=False
        self.reset=False
    def processInputs(self):
        global running

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    running=False

                self.pause=True if event.key==pygame.K_p else False
                    
                self.reset=True if event.key==pygame.K_r else False
                    
                self.rotate=True  if event.key==pygame.K_SPACE or event.key==pygame.K_UP or event.key==pygame.K_w else False
                           

        keys = pygame.key.get_pressed()

        self.left=True if keys[pygame.K_a] or keys[pygame.K_LEFT] else False
        self.right=True if keys[pygame.K_d] or keys[pygame.K_RIGHT] else False
        self.down=True if keys[pygame.K_s] or keys[pygame.K_DOWN] else False         

class TetrisGame:
    def __init__(self, screenX, screenY):
        self.inputHandler=InputHandler()

        self.field=[[0 for x in range(10)] for y in range(20)]
        self.lines=0
        self.score=0
        self.level=0
        self.gameOver=False
        self.paused=False
        self.blockSize=30
        self.nextPieceReady=True

        self.blocks=[
    [#I
     [[0,0,0,0],
      [1,1,1,1],
      [0,0,0,0],
      [0,0,0,0]],

     [[0,0,1,0], 
      [0,0,1,0],
      [0,0,1,0],
      [0,0,1,0]],

     [[0,0,0,0],
      [1,1,1,1],
      [0,0,0,0],
      [0,0,0,0]],
     
     [[0,0,1,0],
      [0,0,1,0],
      [0,0,1,0],
      [0,0,1,0]]
    ],
    
    [#O
     [[2,2],
      [2,2]],

     [[2,2],
      [2,2]],

     [[2,2],
      [2,2]],

     [[2,2],
      [2,2]]
    ],
     
    [#T
     [[0,0,0],
      [3,3,3],
      [0,3,0]],

     [[0,3,0],
      [3,3,0],
      [0,3,0]],

     [[0,3,0],
      [3,3,3],
      [0,0,0]],

     [[0,3,0],
      [0,3,3],
      [0,3,0]]
    ],
    
    [#S
     [[0,0,0],
      [0,4,4],
      [4,4,0]],
    
     [[4,0,0],
      [4,4,0],
      [0,4,0]],
     
     [[0,0,0],
      [0,4,4],
      [4,4,0]],
     
     [[4,0,0],
      [4,4,0],
      [0,4,0]],
    ],
    
    [#Z
     [[0,0,0],
      [5,5,0],
      [0,5,5]], 
       
     [[0,0,5],
      [0,5,5],
      [0,5,0]],
       
     [[0,0,0],
      [5,5,0],
      [0,5,5]],
       
     [[0,0,5],
      [0,5,5],
      [0,5,0]],
    ],
    
    [#J
     [[0,0,0],
      [6,6,6],
      [0,0,6]],

     [[0,6,0],
      [0,6,0],
      [6,6,0]],
    
     [[0,0,0],
      [6,0,0],
      [6,6,6]], 
    
     [[0,6,6],
      [0,6,0],
      [0,6,0]]
    ],
    
    [#L
     [[0,0,0],
      [7,7,7],
      [7,0,0]],
     
     [[7,7,0],
      [0,7,0],
      [0,7,0]],

     [[0,0,0],
      [0,0,7],
      [7,7,7]],

     [[0,7,0],
      [0,7,0],
      [0,7,7]]
    ]
    ]
        
        self.currentFallingPiece=None

        emptyLineCount=0
        block=random.choice(self.blocks)[0]
        for y in block:
            if all(x==0 for x in y):
                emptyLineCount+=1
            else:
                break
        pos=[int((10-len(block[0]))/2),-emptyLineCount-1]
        self.nextFallingPiece=FallingPiece(block,pos,0)

        self.renderer=Renderer(screenX, screenY, 30)

        self.move_delay = 1000
        self.last_move_time = pygame.time.get_ticks()

        self.move_delay_down = 100
        self.last_move_time_down = pygame.time.get_ticks()

        self.move_delay_side = 200
        self.last_move_time_side = pygame.time.get_ticks()
    
    def genFallingBlock(self):
        if not self.nextPieceReady:
            return
        
        self.currentFallingPiece=self.nextFallingPiece
        
        #check how many empty Lines(air) are in the structure to determine spawn point
        emptyLineCount=0
        block=random.choice(self.blocks)[0]
        for y in block:
            if all(x==0 for x in y):
                emptyLineCount+=1
            else:
                break
        pos=[int((10-len(block[0]))/2),-emptyLineCount-1] 
        self.nextFallingPiece=FallingPiece(block,pos,0)

        self.nextPieceReady=False

    def drawFallingBlock(self,draw):
        structure=self.currentFallingPiece.structure
        pos=self.currentFallingPiece.pos
        #drawBlock in field:
        for y in range(pos[1], pos[1]+len(structure)):
            for x in range(pos[0], pos[0]+len(structure[0])):
                if structure[y-pos[1]][x-pos[0]] != 0:
                    if draw and y>=0:
                        self.field[y][x]=structure[y-pos[1]][x-pos[0]] #-startvalue
                    elif y>=0:
                        self.field[y][x]=0
    
    def handleFallingBlock(self):
        if self.nextPieceReady:
            return
        self.drawFallingBlock(False)
        lowestY=0
        for y in range(len(self.currentFallingPiece.structure)):
            for x in range(len(self.currentFallingPiece.structure[y])):
                if self.currentFallingPiece.structure[y][x]!=0:
                    lowestY=y
        lowestY=self.currentFallingPiece.pos[1]+lowestY
        move=True

        if lowestY>-2:
            if lowestY>=19:
                move=False
                self.drawFallingBlock(True)
                self.checkLine()
                self.nextPieceReady=True
                return
            else:
                for y in range(len(self.currentFallingPiece.structure)):
                    for x in range(len(self.currentFallingPiece.structure[0])):
                        if self.currentFallingPiece.structure[y][x]!=0 and self.currentFallingPiece.pos[1]+y+1>=0:
                            if self.field[self.currentFallingPiece.pos[1]+y+1][self.currentFallingPiece.pos[0]+x]!=0:
                                move=False
                                self.drawFallingBlock(True)
                                self.checkLine()
                                self.nextPieceReady=True
                                return
        if move:
            self.currentFallingPiece.pos[1]+=1
        self.drawFallingBlock(True)

    def moveFallingBlock(self,dir):
        self.drawFallingBlock(False)
        offset= 1 if dir=="right" else -1
        move=True

        minX=100 #erster Block (1) in X
        maxX=-1 #letzter Block in X

        for y in self.currentFallingPiece.structure:
            for x in range(len(y)):
                if y[x]!=0:
                    if x<minX:
                        minX=x
                    elif x>maxX:
                        maxX=x

        if (self.currentFallingPiece.pos[0]+minX<=0 and dir=="left") or (self.currentFallingPiece.pos[0]+maxX>=9 and dir=="right"):
            move=False
        else:
            for y in range(len(self.currentFallingPiece.structure)):
                for x in range(len(self.currentFallingPiece.structure[0])):
                    try:
                        if self.currentFallingPiece.structure[y][x]!=0: #Luft neben block
                            if self.field[self.currentFallingPiece.pos[1]+y][self.currentFallingPiece.pos[0]+x+offset]!=0:
                                move=False
                    except: #auch Luft neben Block da oben Error
                        try:
                            if self.field[self.currentFallingPiece.pos[1]+y][self.currentFallingPiece.pos[0]+x+offset]!=0:
                                move=False
                        except: #Block ganz unten deswegen y index out of range
                            move=False

        if move:
            self.currentFallingPiece.pos[0]+=offset
        self.drawFallingBlock(True)

    def rotate(self):
        rotate=True
        self.drawFallingBlock(False)
        blockNum=-1
        for y in self.currentFallingPiece.structure:
            for x in y:
                if x !=0:
                    blockNum=x-1

        #check rotation
        pos=self.currentFallingPiece.pos
        rotatedStructure=self.blocks[blockNum][(self.currentFallingPiece.rotation+1)%4]
        
        minX=100 #erster Block (1) in X
        maxX=-1 #letzter Block in X

        for y in rotatedStructure:
            for x in range(len(y)):
                if y[x]!=0:
                    if x<minX:
                        minX=x
                    elif x>maxX:
                        maxX=x

        if self.currentFallingPiece.pos[0]+minX<0 or self.currentFallingPiece.pos[0]+maxX>9:
            rotate=False
        else:
            for y in range(len(rotatedStructure)):
                for x in range(len(rotatedStructure[0])):
                    if rotatedStructure[y][x]!=0 and self.field[pos[1]+y][pos[0]+x]!=0: #Block in structure und Block im Field überlappen sich
                        rotate=False

        if rotate:
            self.currentFallingPiece.structure=rotatedStructure
            self.currentFallingPiece.rotation+=1
        self.drawFallingBlock(True)

    def checkLine(self):
        newField=[]
        linesCleared=0
        for y in range(len(self.field)):
            if 0 not in self.field[y]:
                linesCleared+=1
                self.lines+=1
                self.renderer.highlightLine(y)
            else:
                newField.append(self.field[y])
        
        match(linesCleared):
            case 1:
                self.score+=100*(self.level+1)
            case 2:
                self.score+=300*(self.level+1)
            case 3:
                self.score+=500*(self.level+1)
            case 4:
                self.score+=800*(self.level+1)

        for _ in range(linesCleared):
            newField.insert(0, [0 for x in range(10)])
        
        self.renderer.drawScore(self.lines,self.score,self.level)
        self.field=newField

    def checkGameOver(self):
        if (self.field[0][3] !=0 or self.field[0][4] !=0 or self.field[0][4]!=0 or self.field[0][4] !=0) and self.nextPieceReady:
            self.gameOver=True
            self.renderer.highlightGameOver()

    def reset(self):
        self.lines=0
        self.score=0
        self.level=0
        self.field=[[0 for x in range(10)] for y in range(20)]
        self.currentFallingPiece=None
        self.nextPieceReady=True
        self.gameOver=False
        self.paused=False
        self.renderer.drawScore(0,0,0)
        pygame.draw.rect(self.renderer.screen, (0, 0, 0), (0, 0, 500, 600))

    def run(self):
        self.renderer.clearScreen()
        self.inputHandler.processInputs()

        if self.gameOver:
            self.renderer.drawGameOver()
            keys=pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game.reset()
            pygame.display.update()
            return
        
        if self.inputHandler.pause:
            self.inputHandler.pause=False
            self.paused=not self.paused

        if self.paused:
            self.renderer.drawPause()
            pygame.display.update()
            return

        self.level=self.lines//10 if self.lines<=99 else 9
        self.move_delay=1000-self.level*100
        self.renderer.drawField(self.field)
        self.renderer.drawScore(self.lines,self.score,self.level)
        self.genFallingBlock()
        self.renderer.drawPreview(self.nextFallingPiece)

        if self.inputHandler.rotate:
            self.inputHandler.rotate=False
            self.rotate()
        
        if self.inputHandler.reset:
            self.inputHandler.reset=False
            self.reset()

        now=pygame.time.get_ticks()

        if now-self.last_move_time_side>=self.move_delay_side and self.inputHandler.left:
                self.moveFallingBlock("left")
                self.last_move_time_side=now
        
        if now-self.last_move_time_side>=self.move_delay_side and self.inputHandler.right:
                self.moveFallingBlock("right")
                self.last_move_time_side=now

        if now-self.last_move_time_down>=self.move_delay_down and self.inputHandler.down:
                self.handleFallingBlock()
                self.last_move_time_down=now

        if now-self.last_move_time>=self.move_delay: 
            game.handleFallingBlock()
            self.checkGameOver()
            self.last_move_time=now
            
        self.renderer.updateGameScreen()

class FallingPiece:
    def __init__(self, structure, pos, rotation):
        self.structure=structure
        self.pos=pos
        self.rotation=rotation

class Renderer:
    def __init__(self, screenX, screenY, blockSize):
        self.blockSize=blockSize
        self.screenX=screenX
        self.screenY=screenY
        self.screen=pygame.display.set_mode((screenX,screenY))
        self.surface=pygame.Surface((self.blockSize*10,self.blockSize*20))
        self.surfacePreview=pygame.Surface((self.blockSize*4,self.blockSize*4))
        self.textSurface = my_font1.render('0', False, (255, 255, 255))
        self.menuSurface = my_font1.render('0', False, (255, 255, 255))

        self.block_colors=[
    (30,30,30),      # empty
    (0, 255, 255),   # I
    (255, 255, 0),   # O
    (160, 0, 240),   # T
    (0, 255, 0),     # S
    (255, 0, 0),     # Z
    (0, 0, 255),     # J
    (255, 128, 0),   # L
    (255, 255, 255)  #Full Line
]
        
    def clearScreen(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screenX, self.screenY))

    def drawField(self, field):
        rect=pygame.Rect((0,0),(10*self.blockSize,20*self.blockSize))
        pygame.draw.rect(self.surface, (0,0,0), rect)
        for y in range(len(field)):
            for x in range(len(field[0])):
                innerRect=pygame.Rect((x*self.blockSize+5,y*self.blockSize+5),(self.blockSize-10,self.blockSize-10))
                pygame.draw.rect(self.surface, self.block_colors[field[y][x]], innerRect)
    
    def drawPreview(self, nextFallingPiece):
        structure=nextFallingPiece.structure
        for y in range(4):
            for x in range(4):
                innerRect=pygame.Rect((x*self.blockSize+5,y*self.blockSize+5),(self.blockSize-10,self.blockSize-10))
                pygame.draw.rect(self.surfacePreview, (0,0,0), innerRect)

        for y in range(len(nextFallingPiece.structure)):
            for x in range(len(nextFallingPiece.structure[0])):
                innerRect=pygame.Rect((x*self.blockSize+5,y*self.blockSize+5),(self.blockSize-10,self.blockSize-10))
                if structure[y][x]!=0:
                    pygame.draw.rect(self.surfacePreview, self.block_colors[structure[y][x]], innerRect)
    
    def highlightLine(self,y):
        for x in range(5):
            innerRect1=pygame.Rect(((4-x)*self.blockSize+5,y*self.blockSize+5),(self.blockSize-10,self.blockSize-10))
            innerRect2=pygame.Rect(((5+x)*self.blockSize+5,y*self.blockSize+5),(self.blockSize-10,self.blockSize-10))
            pygame.draw.rect(self.surface, (30,30,30), innerRect1)
            pygame.draw.rect(self.surface, (30,30,30), innerRect2)
            self.screen.blit(self.surface,(0,0))
            pygame.display.update()
            highlight_delay = 50  # milliseconds
            last_time = pygame.time.get_ticks()
            while True:
                now = pygame.time.get_ticks()
                if now-last_time>=highlight_delay:
                    break
        highlight_delay = 100  # milliseconds
        last_time = pygame.time.get_ticks()
        while True:
            now = pygame.time.get_ticks()
            if now-last_time>=highlight_delay:
                break
    
    def highlightGameOver(self):
        for x in range(5):
            for y in range(20):
                innerRect1=pygame.Rect(((4-x)*self.blockSize+5,y*self.blockSize+5),(self.blockSize-10,self.blockSize-10))
                innerRect2=pygame.Rect(((5+x)*self.blockSize+5,y*self.blockSize+5),(self.blockSize-10,self.blockSize-10))
                pygame.draw.rect(self.surface, (255,255,255), innerRect1)
                pygame.draw.rect(self.surface, (255,255,255), innerRect2)
            self.screen.blit(self.surface,(0,0))
            highlight_delay = 100  # milliseconds
            last_time = pygame.time.get_ticks()
            while True:
                now = pygame.time.get_ticks()
                if now-last_time>=highlight_delay:
                    break
            pygame.display.update()

        highlight_delay = 500  # milliseconds
        last_time = pygame.time.get_ticks()
        while True:
            now = pygame.time.get_ticks()
            if now-last_time>=highlight_delay:
                break

    def drawScore(self,lines,score,level):
        self.textSurface = my_font2.render(f'Score', False, (255, 255, 255))
        self.screen.blit(self.textSurface,(310,200))
        self.textSurface = my_font2.render(f'{score}', False, (150, 150, 150))
        self.screen.blit(self.textSurface,(310,230))

        self.textSurface = my_font2.render(f'Lines', False, (255, 255, 255))
        self.screen.blit(self.textSurface,(310,280))
        self.textSurface = my_font2.render(f'{lines}', False, (150, 150, 150))
        self.screen.blit(self.textSurface,(310,310))

        self.textSurface = my_font2.render(f'Level', False, (255, 255, 255))
        self.screen.blit(self.textSurface,(310,360))
        self.textSurface = my_font2.render(f'{level}', False, (150, 150, 150))
        self.screen.blit(self.textSurface,(310,390))
    
    def drawGameOver(self):
        self.menuSurface = my_font1.render('GAME OVER', False, (255, 0, 0))
        self.screen.blit(self.menuSurface, (40,220))
        self.menuSurface = my_font2.render('R TO TRY AGAIN', False, (170, 0, 0))
        self.screen.blit(self.menuSurface, (115,280))
        pygame.display.update()

    def drawPause(self):
        self.menuSurface = my_font1.render('Paused', False, (0, 0, 255))
        self.screen.blit(self.menuSurface, (130,220))

        self.menuSurface = my_font2.render('P TO Resume', False, (0, 0, 170))
        self.screen.blit(self.menuSurface, (140,280))
        pygame.display.update()
    
    def updateGameScreen(self):
        self.screen.blit(self.surface,(0,0))
        self.screen.blit(self.surfacePreview,(330,0))
        pygame.display.update()

pygame.init()
pygame.font.init()
my_font1 = pygame.font.SysFont('Ascender Sans Mono', 100)
my_font2 = pygame.font.SysFont('Ascender Sans Mono', 50)

pygame.display.set_caption("PyTris")

game=TetrisGame(500,600)

running=True

while running:
    game.run()
        
pygame.quit()