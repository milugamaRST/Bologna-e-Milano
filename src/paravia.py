#
# paravia.py
#
# /**********************************************************************************
# **                                                                               **
# ** Santa Paravia & Fiumaccio. Traduzido do código fonte original do TRS-80 BASIC **
# ** para C por Thomas Knox <tknox@mac.com>.                                       **
# ** adaptado para Python por Andreas Grimm <andreas.grimm@gricom.eu               **
# **                                                                               **
# ** Programa original (C) 1979 por George Blank                                   **
# ** <gwblank@postoffice.worldnet.att.net>                                         **
# **                                                                               **
# ***********************************************************************************
#
# Copyright (C) 2000 Thomas Knox
#
# Partes Copyright (C) 1979 por George Blank, usado com permissão. Este programa é
# software livre; você pode redistribuí-lo e/ou modificá-lo sob os termos da
# Licença Pública Geral GNU como publicada pela Free Software Foundation; seja a versão 2
# da Licença, ou (a seu critério) qualquer versão posterior. Este programa é distribuído
# na esperança de que seja útil, mas SEM QUALQUER GARANTIA; sem mesmo a garantia
# implícita de COMERCIALIZAÇÃO ou ADEQUAÇÃO A UMA FINALIDADE ESPECÍFICA. Veja a
# Licença Pública Geral GNU para mais detalhes. Você deve ter recebido uma cópia da
# Licença Pública Geral GNU junto com este programa; se não, escreva para a Free
# Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# Thomas Knox
# tknox@mac.com

import random

from gameClasses import player
from infrastructure import common

cityList = ["Santa Paravia", "Fiumaccio", "Torricella", "Molinetto", "Fontanile", "Romanga", "Monterana"]
players = []


def instructions():
    print("Santa Paravia e Fiumaccio\n")
    print(
        "Você é o governante de uma cidade-estado italiana do século XV. Se governar bem, receberá títulos mais altos. O primeiro")
    print(
        "jogador a se tornar rei ou rainha vence. A expectativa de vida naquela época era breve, então você pode não viver")
    print(
        "tempo suficiente para vencer. O computador irá desenhar um mapa do seu estado. O tamanho da área dentro da muralha")
    print(
        "cresce à medida que você compra mais terras. O tamanho da torre de guarda no canto superior esquerdo mostra a")
    print(
        "adequação de suas defesas. Se ela diminuir, equipe mais soldados! Se o cavalo e o lavrador estiverem tocando o topo")
    print(
        "da muralha, toda a sua terra está em produção. Caso contrário, você precisa de mais servos, que migrarão para o seu")
    print(
        "estado se você distribuir mais grãos do que a demanda mínima. Se você distribuir menos grãos, algumas pessoas")
    print(
        "irão morrer de fome e você terá uma alta taxa de mortalidade. Altos impostos aumentam o dinheiro, mas")
    input("retardam o crescimento econômico.\n\n(Pressione ENTER para começar o jogo)")


def playGame():
    allDead = False

    evilBaron = player.Player("Peppone", "male")

    while True:
        for currentPlayer in players:
            if currentPlayer.isDead == False:
                newTurn(currentPlayer=currentPlayer, evilBaron=evilBaron)

        allDead = True;
        for currentPlayer in players:
            if allDead == True and currentPlayer.isDead == False:
                allDead = False

        for currentPlayer in players:
            if currentPlayer.iWon == True:
                print("Fim de Jogo. " + currentPlayer.getTitle() + " " + currentPlayer.name + " vence.")
                return

        if allDead == True:
            print("O jogo terminou.\n");
            break


def isDead(currentPlayer):
    print("\n\nNotícias muito tristes.\n" + currentPlayer.title + currentPlayer.name + " acabou de morrer")

    if currentPlayer.year > 1450:
        print("de velhice após um longo reinado.\n")
    else:
        why = random.randint(0, 8)
        deathReason = {
            0: "",
            1: "",
            2: "",
            3: "de pneumonia após um inverno frio em um castelo com muitas correntes de ar.",
            4: "de febre tifoide após beber água contaminada.",
            5: "em uma epidemia de varíola.",
            6: "após ser atacado por ladrões durante uma viagem.",
            7: "",
            8: "de intoxicação alimentar."
        }
        print(deathReason[why])

    currentPlayer.isDead = True

    input("\n(Pressione ENTER): ")


def printGrain(harvest):
    harvestRating = {
        1: "Estiagem. Ameaça de Fome. ",
        2: "Mau Tempo. Colheita Fraca. ",
        3: "Tempo Normal. Colheita Média. ",
        4: "Bom Tempo. Boa Colheita. ",
        5: "Tempo Excelente. Ótima Colheita! "
    }
    print(harvestRating[int(harvest)])


def buySellGrain(currentPlayer):
    finished = False
    while (finished == False):
        print("\n==================================================================================================\n")
        print("\nAno " + str(currentPlayer.year))
        print("\n" + currentPlayer.getTitle() + " " + currentPlayer.name)
        print("\nRatos comeram " + str(currentPlayer.rats) + "% de suas reservas de grãos. ({0:.0f} steres)".format(
            currentPlayer.ratsAte))
        printGrain(currentPlayer.harvest)
    
        print (f"Reserva de grãos: {currentPlayer.grainReserve:.0f} steres.")
        mensagem=f"Demanda de grãos: {currentPlayer.grainDemand:.0f} steres. {"Boa reserva! Temos alimento suficiente para o povo." if currentPlayer.grainDemand<currentPlayer.grainReserve*.8 else "Teremos fome!❌"}"
        print (f"{mensagem}")
        print (f"Preço do grão: {currentPlayer.grainPrice:.2f} /1000 steres.")
        print (f"Preço da terra: {currentPlayer.landPrice:.2f} /hectare.")
        print (f"Saldo do tesouro: {currentPlayer.treasury:.0f} florins.")

        print("\nReserva de\t\tDemanda de\t\tPreço do\t\tPreço do\t\tTesouro")
        print("Grãos\t\tGrãos\t\tGrão\t\tTerreno\n")
        print(" {0:>10.2f}\t{1:>10.2f}\t{2:>10.2f}\t\t{3:>4.2f}\t\t{4:>4.2f}\n".format(currentPlayer.grainReserve,
                                                                                       currentPlayer.grainDemand,
                                                                                       currentPlayer.grainPrice,
                                                                                       currentPlayer.landPrice,
                                                                                       currentPlayer.treasury))
        print("steres\t\tsteres\t\t1000 st.\thectare\t\tflorins de ouro\n")
        print("\nVocê tem " + str(currentPlayer.land) + " hectares de terra.")
        print("\n1. Comprar grãos, 2. Vender grãos, 3. Comprar terras, 4. Vender terras ")

        select = input("(Pressione q para continuar):")
        if select == 'q':
            finished = True

        if select == '1':
            amount = common.Numbers.inputInt("Quantos grãos você deseja comprar (0 para especificar um total)? ")
            if amount == 0:
                amount = int(input("Qual o total de grãos que você deseja? "))
                amount = amount - currentPlayer.grainReserve
            if amount < 0:
                print("Quantidade total inválida.\n")
                return
            currentPlayer.buyGrain(amount)

        if select == '2':
            amount = common.Numbers.inputInt("Quantos grãos você deseja vender (0 para especificar um total)? ")
            if amount == 0:
                amount = int(input("Qual o total de grãos que você deseja? "))
                amount = currentPlayer.grainReserve - amount
            if amount < 0:
                print("Quantidade total inválida.\n")
                return
            currentPlayer.sellGrain(amount)

        if select == '3':
            amount = common.Numbers.inputInt("Quantas terras você deseja comprar (0 para especificar um total)? ")
            if amount == 0:
                amount = int(input("Qual o total de terras que você deseja? "))
                amount = amount - currentPlayer.land
            if amount < 0:
                print("Quantidade total inválida.\n")
                return
            currentPlayer.buyLand(amount)

        if select == '4':
            amount = common.Numbers.inputInt("Quantas terras você deseja vender (0 para especificar um total)? ")
            if amount == 0:
                amount = int(input("Qual o total de terras que você deseja? "))
                amount = currentPlayer.land - amount
            if amount < 0:
                print("Quantidade total inválida.\n")
                return
            currentPlayer.sellLand(amount)


def showStats():
    print("    Nobres\t   Soldados\t    Clero\t Comerciantes\t     Servos\t      Terra\t  Tesouro\n")
    for x in players:
        print("\n" + x.getTitle() + " " + x.name)
        print("{0:>10.2f}\t{1:>10.2f}\t{2:>10.0f}\t{3:>10.0f}\t{4:10.0f}\t{5:10.0f}\t{6:>10.2f}\n".format(x.nobles,
                                                                                                          x.soldiers,
                                                                                                          x.clergy,
                                                                                                          x.merchants,
                                                                                                          x.serfs,
                                                                                                          x.land,
                                                                                                          x.treasury))
        input("\n(Pressione ENTER): ")


def statePurchases(currentPlayer):
    choice = ""
    while choice != 'q':
        print("\n\n" + currentPlayer.getTitle() + " " + currentPlayer.name + "\nCompras do Estado.")
        print("1. Mercado ({0:.2f})\t\t\t\t1000 florins\n".format(currentPlayer.marketplaces))
        print("2. Moinho de lã ({0:.2f})\t\t\t\t2000 florins\n".format(currentPlayer.mills))
        print("3. Palácio (parcial) ({0:.2f})\t\t\t3000 florins\n".format(currentPlayer.palace))
        print("4. Catedral (parcial) ({0:.2f})\t\t\t5000 florins\n".format(currentPlayer.cathedral))
        print("5. Equipar um pelotão de servos como soldados\t500 florins\n")
        print("\nVocê tem {0:.2f} florins de ouro.\n".format(currentPlayer.treasury))
        print("\nPara continuar, pressione q. Para comparar pontuações, pressione 6\n");
        choice = input("Sua escolha: ")
        if choice == "1":
            currentPlayer.buyMarket()
        elif choice == "2":
            currentPlayer.buyMill()
        elif choice == "3":
            currentPlayer.buyPalace()
        elif choice == "4":
            currentPlayer.buyCathedral()
        elif choice == "5":
            currentPlayer.buySoldiers()
        elif choice == "6":
            showStats()


def newTurn(currentPlayer, evilBaron):
    currentPlayer.harvestLandAndGrainPrices()
    currentPlayer.ratLoss()
    buySellGrain(currentPlayer)
    currentPlayer.releaseGrain()

    print ("=========================================================================")

    attacked = False
    if currentPlayer.invadeMe == True:
        for opponent in players:
            if opponent != currentPlayer:
                if opponent.soldiers > int(currentPlayer.soldiers * 2.4):
                    currentPlayer.attackedByNeighbor(opponent)
                    attacked = True

        if attacked != True:
            currentPlayer.attackedByNeighbor(evilBaron)

    currentPlayer.adjustTax()

    # if the player is bankrupt, seize the assets
    if currentPlayer.isBankrupt == True:
        currentPlayer.seizeAssets()
        print("\n" + + currentPlayer.getTitle() + " " + currentPlayer.name + " está falido.")
        print("\nCredores confiscaram muitos de seus bens.")
        input("(Pressione ENTER): ")

    # DrawMap(Me);
    statePurchases(currentPlayer)
    currentPlayer.checkNewTitle()

    currentPlayer.year = currentPlayer.year + 1

    # if currentPlayer.year == currentPlayer.yearOfDeath:
    #    currentPlayer.imDead()
    if currentPlayer.title >= 7:
        currentPlayer.iWon = True


def main():
    try:
        # Start the game
        print("Santa Paravia e Fiumaccio\n\n")
        answer = input("Deseja instruções (S ou N)? ")

        if answer == 's' or answer == 'S':
            instructions()

        numOfPlayers = int(input("Quantas pessoas querem jogar (1 a 6)? "))

        if numOfPlayers < 1 or numOfPlayers > 6:
            print("Obrigado por jogar.\n")
            return

        print("\nQual será a dificuldade deste jogo:\n\n1. Aprendiz")
        print("2. Jornaleiro\n3. Mestre\n4. Grão-Mestre\n")
        level = int(input("Escolha: "))

        if level < 1:
            level = 1

        if level > 4:
            level = 4

        for counter in range(numOfPlayers):
            name = input("Quem é o governante de " + cityList[counter] + "? ")
            name = name.rstrip()

            genderAnswer = input("" + name + " é um homem ou uma mulher (H ou M)? ")
            if genderAnswer == 'h' or genderAnswer == 'H':
                gender = "male"
            else:
                gender = "female"

            currentPlayer = player.Player(name, gender)
            currentPlayer.difficulty = level
            players.append(currentPlayer)

        # Enter the main game loop.
        playGame()

    except KeyboardInterrupt:
        print("\nJogo terminado pelo jogador")

    # We're finished.
    return


main()
