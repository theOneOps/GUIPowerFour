#
# def fill_cell(canvas, row, col, humanColor: str, botColor: str, height: int,
#               width: int, tokens: int):
#     global tab
#     global nbSquareFilled
#     global tourJeu
#     global stack
#     global finishG
#
#     minWidthHeight: int = min([width, height])
#
#     if finishG:
#         if nbSquareFilled < height * width:
#             if tab[row][col] == -1:
#                 for row in range(height - 1, -1, -1):
#                     if tab[row][col] == -1:
#                         tab[row][col] = 1
#                         thePosition: Pos_t = [row, col]
#                         # adding to the stack
#                         stack.append(thePosition)
#                         finishG = launchGame(tab, width, height,
#                                              tourJeu=tourJeu,
#                                              tokens=tokens, pile=stack,
#                                              finishGame=finishG,
#                                              thePos=thePosition)
#                         # For example, you can change the color of the circle when clicked
#                         canvas.itemconfig(f"circle_{row}_{col}",
#                                           fill=f"{humanColor}")
#                         nbSquareFilled += 1
#                         if not (finishG):
#                             tkinter.messagebox.showinfo("victoire",
#                                                         "Vous avez gagné !")
#                             return
#                         break
#             tourJeu += 1
#         else:
#             tkinter.messagebox.showinfo("match nul",
#                                         "pas de gagnant")
#             return
#         print(f"the finishGame : {finishG}")
#
#     else:
#         tkinter.messagebox.showinfo("fin du jeu", "on a déjà un gagnant !")
#         return
#
#     if finishG:
#         if nbSquareFilled < height * width:
#             thePosition: Pos_t = getRandomPosition(tab, width, height)
#             for row in range(height - 1, -1, -1):
#                 if tab[row][thePosition[1]] == -1:
#                     tab[row][thePosition[1]] = 0
#                     # adding to the stack
#                     stack.append([row, thePosition[1]])
#                     finishG = launchGame(tab, width, height,
#                                          tourJeu=tourJeu,
#                                          tokens=tokens, pile=stack,
#                                          finishGame=finishG,
#                                          thePos=[row,
#                                                  thePosition[1]])
#                     # For example, you can change the color of the circle when clicked
#                     canvas.itemconfig(f"circle_{row}_{thePosition[1]}",
#                                       fill=f"{botColor}")
#                     nbSquareFilled += 1
#                     if not (finishG):
#                         tkinter.messagebox.showinfo("victoire",
#                                                     "Le bot a gagné !")
#                         return
#                     break
#             tourJeu += 1
#         else:
#             tkinter.messagebox.showinfo("match nul",
#                                         "pas de gagnant")
#             return
#     else:
#         tkinter.messagebox.showinfo("fin du jeu", "on a déjà un gagnant !")
#         return
#
#
# def comeBackFunc(canvas: Canvas):
#     global tab
#     global stack
#     oldPosition: Pos_t = peek(stack)
#     if oldPosition is not None:
#         canvas.itemconfig(f"circle_{oldPosition[0]}_{oldPosition[1]}",
#                           fill="white")
#         tab[oldPosition[0]][oldPosition[1]] = -1
#         stack.pop()
#
#
# def bestPositionFunc(canvas: Canvas, width: int, height: int, tokens: int,
#                      humanColor: str, botColor: str):
#     global tab
#     global nbSquareFilled
#     global tourJeu
#     global stack
#     global finishG
#
#     minWidthHeight: int = min([width, height])
#
#     if finishG:
#         if nbSquareFilled < height * width:
#             thePosition: Pos_t = getRandomPosition(tab, width, height)
#             for row in range(height - 1, -1, -1):
#                 if tab[row][thePosition[1]] == -1:
#                     tab[row][thePosition[1]] = 1
#                     # adding to the stack
#                     stack.append([row, thePosition[1]])
#                     finishG = launchGame(tab, width, height,
#                                          tourJeu=tourJeu,
#                                          tokens=tokens, pile=stack,
#                                          finishGame=finishG,
#                                          thePos=[row,
#                                                  thePosition[1]])
#                     # For example, you can change the color of the circle when clicked
#                     canvas.itemconfig(f"circle_{row}_{thePosition[1]}",
#                                       fill=f"{humanColor}")
#                     nbSquareFilled += 1
#                     if not (finishG):
#                         tkinter.messagebox.showinfo("victoire",
#                                                     "Vous avez gagné !")
#                         return
#                     break
#             tourJeu += 1
#         else:
#             tkinter.messagebox.showinfo("match nul",
#                                         "pas de gagnant")
#             return
#     else:
#         tkinter.messagebox.showinfo("fin du jeu", "on a déjà un gagnant !")
#         return
#
#     if finishG:
#         if nbSquareFilled < height * width:
#             thePosition: Pos_t = getRandomPosition(tab, width, height)
#             for row in range(height - 1, -1, -1):
#                 if tab[row][thePosition[1]] == -1:
#                     tab[row][thePosition[1]] = 0
#                     # adding to the stack
#                     stack.append([row, thePosition[1]])
#                     finishG = launchGame(tab, width, height,
#                                          tourJeu=tourJeu,
#                                          tokens=tokens, pile=stack,
#                                          finishGame=finishG,
#                                          thePos=[row,
#                                                  thePosition[1]])
#                     # For example, you can change the color of the circle when clicked
#                     canvas.itemconfig(f"circle_{row}_{thePosition[1]}",
#                                       fill=f"{botColor}")
#                     nbSquareFilled += 1
#                     if not (finishG):
#                         tkinter.messagebox.showinfo("victoire",
#                                                     "Le bot a gagné !")
#                         return
#                     break
#             tourJeu += 1
#         else:
#             tkinter.messagebox.showinfo("match nul",
#                                         "pas de gagnant")
#             return
#     else:
#         tkinter.messagebox.showinfo("fin du jeu", "on a déjà un gagnant !")
#         return
