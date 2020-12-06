import socket
import time
from _thread import *
import json
import requests
from random import randint

# URL for the update player lambda function
URL = "https://s95l8llb78.execute-api.us-east-2.amazonaws.com/default/updatePlayerInfo"
API_KEY = "cfHmIMAww52kOROgW1L4932hBphr1rWt82QKZtqs"
sendToAddress = ()

players = {
    "0": {"name":"Joss"},
    "1": {"name":"Tom"},
    "2": {"name":"Catherine"},
    "3": {"name":"David"},
    "4": {"name":"Alex"},
    "5": {"name":"Rachel"},
    "6": {"name":"Michael"},
    "7": {"name":"Paige"},
    "8": {"name":"Duncan"},
    "9": {"name":"Mila"}
}
# Passed as a string to the server that converts it to int
numGames = '10'
kVal = 30

def ConnectToServer(sock):
    msg = {'cmd':'connect', 'gameCount':numGames}
    m = json.dumps(msg)
    print("Sending Connection...")
    sock.sendto(bytes(m, 'utf8'), sendToAddress)

def heartbeat(sock):
    while True:
        msg = 'heartbeat'
        #print("Sending Heartbeat...")
        sock.sendto(bytes(msg, 'utf8'), sendToAddress)
        time.sleep(3)

def connectionLoop(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        data = str(data)
        if 'gameID' in data:
            print("Received Game\n")
            SimulateGame(data[2:-1], sock)
        time.sleep(1)

def SimulateGame(data, sock):
    #print(data)
    player1Key = json.loads(data)['player1Key']
    player2Key = json.loads(data)['player2Key']
    player3Key = json.loads(data)['player3Key']

    gamePlayers = {}
    gamePlayers[player1Key] = {}
    gamePlayers[player1Key]['name'] = json.loads(data)[player1Key]['name']
    gamePlayers[player1Key]['rating'] = json.loads(data)[player1Key]['rating']

    gamePlayers[player2Key] = {}
    gamePlayers[player2Key]['name'] = json.loads(data)[player2Key]['name']
    gamePlayers[player2Key]['rating'] = json.loads(data)[player2Key]['rating']

    gamePlayers[player3Key] = {}
    gamePlayers[player3Key]['name'] = json.loads(data)[player3Key]['name']
    gamePlayers[player3Key]['rating'] = json.loads(data)[player3Key]['rating']


    print("Game " + str(json.loads(data)['gameID']) + ":")
    print(gamePlayers[player1Key]['name'] + "(" + str(gamePlayers[player1Key]['rating']) + "), " +
            gamePlayers[player2Key]['name'] + "(" + str(gamePlayers[player2Key]['rating']) + "), " +
            gamePlayers[player3Key]['name'] + "(" + str(gamePlayers[player3Key]['rating']) + ")")
    
    logFile = open("GameRecord.txt", "w")
    logFile.write("Game " + str(json.loads(data)['gameID']) + ":")
    logFile.write(gamePlayers[player1Key]['name'] + "(" + str(gamePlayers[player1Key]['rating']) + "), " +
                    gamePlayers[player2Key]['name'] + "(" + str(gamePlayers[player2Key]['rating']) + "), " +
                    gamePlayers[player3Key]['name'] + "(" + str(gamePlayers[player3Key]['rating']) + ")")
    
    gameOutcome = {}
    gameOutcome[player1Key] = randint(0, 50)
    gameOutcome[player2Key] = randint(0, 50)
    gameOutcome[player3Key] = randint(0, 50)

    if gameOutcome[player1Key] > gameOutcome[player2Key]:
        if gameOutcome[player1Key] > gameOutcome[player3Key]:
            if gameOutcome[player2Key] > gameOutcome[player3Key]:
                PrintOutcome(gamePlayers[player1Key]['name'], gamePlayers[player2Key]['name'], gamePlayers[player3Key]['name'], logFile)
                gamePlayers[player1Key]['rating'], gamePlayers[player2Key]['rating'], gamePlayers[player3Key]['rating'] = (
                    CalculateNewRating(gamePlayers[player1Key]['rating'], gamePlayers[player2Key]['rating'], gamePlayers[player3Key]['rating']))
            else:
                PrintOutcome(gamePlayers[player1Key]['name'], gamePlayers[player3Key]['name'], gamePlayers[player2Key]['name'], logFile)
                gamePlayers[player1Key]['rating'], gamePlayers[player3Key]['rating'], gamePlayers[player2Key]['rating'] = (
                    CalculateNewRating(gamePlayers[player1Key]['rating'], gamePlayers[player3Key]['rating'], gamePlayers[player2Key]['rating']))
        else:
            PrintOutcome(gamePlayers[player3Key]['name'], gamePlayers[player1Key]['name'], gamePlayers[player2Key]['name'], logFile)
            gamePlayers[player3Key]['rating'], gamePlayers[player1Key]['rating'], gamePlayers[player2Key]['rating'] = (
                    CalculateNewRating(gamePlayers[player3Key]['rating'], gamePlayers[player1Key]['rating'], gamePlayers[player2Key]['rating']))
    else:
        if gameOutcome[player2Key] > gameOutcome[player3Key]:
            if gameOutcome[player1Key] > gameOutcome[player3Key]:
                PrintOutcome(gamePlayers[player2Key]['name'], gamePlayers[player1Key]['name'], gamePlayers[player3Key]['name'], logFile)
                gamePlayers[player2Key]['rating'], gamePlayers[player1Key]['rating'], gamePlayers[player3Key]['rating'] = (
                    CalculateNewRating(gamePlayers[player2Key]['rating'], gamePlayers[player1Key]['rating'], gamePlayers[player3Key]['rating']))
            else:
                PrintOutcome(gamePlayers[player2Key]['name'], gamePlayers[player3Key]['name'], gamePlayers[player1Key]['name'], logFile)
                gamePlayers[player2Key]['rating'], gamePlayers[player3Key]['rating'], gamePlayers[player1Key]['rating'] = (
                    CalculateNewRating(gamePlayers[player2Key]['rating'], gamePlayers[player3Key]['rating'], gamePlayers[player1Key]['rating']))
        else:
            PrintOutcome(gamePlayers[player3Key]['name'], gamePlayers[player2Key]['name'], gamePlayers[player1Key]['name'], logFile)
            gamePlayers[player3Key]['rating'], gamePlayers[player2Key]['rating'], gamePlayers[player1Key]['rating'] = (
                    CalculateNewRating(gamePlayers[player3Key]['rating'], gamePlayers[player2Key]['rating'], gamePlayers[player1Key]['rating']))
    
    print(gamePlayers[player1Key]['name'] + "(" + str(gamePlayers[player1Key]['rating']) + "), " +
            gamePlayers[player2Key]['name'] + "(" + str(gamePlayers[player2Key]['rating']) + "), " +
            gamePlayers[player3Key]['name'] + "(" + str(gamePlayers[player3Key]['rating']) + ")")
    UpdateDatabase(gamePlayers)
    ReConnectPlayers(gamePlayers, sock)

def PrintOutcome(first, second, third, log):
    print(first + " came in first.")
    print(second + " came in second.")
    print(third + " came in third.")
    log.write(first + " came in first.")
    log.write(second + " came in second.")
    log.write(third + " came in third.")

def UpdateDatabase(temp):
    for p in temp:
        data = {'player_id':p,
                'name':temp[p]['name'],
                'rating':temp[p]['rating']}
        requests.post(url = URL, params = data)
        #print(r)

def ReConnectPlayers(temp, sock):
    for p in temp:
        message = {"cmd":"playerConnect", "id":p, "name":temp[p]["name"]}
        m = json.dumps(message)
        sock.sendto(bytes(m, 'utf8'), sendToAddress)

def CalculateNewRating(first, second, third):
    first = int(first)
    second = int(second)
    third = int(third)

    firstModExp = 2 * (ExpectedValue(first, second) + ExpectedValue(first, third) / 2) / 3
    firstNewRating = NewScore(first, firstModExp, 1.0)

    secModExp = 2 * (ExpectedValue(second, first) + ExpectedValue(second, third) / 2) / 3
    secNewRating = NewScore(second, secModExp, 0.5)

    thirdModExp = 2 * (ExpectedValue(third, first) + ExpectedValue(third, second) / 2) / 3
    thirdNewRating = NewScore(third, thirdModExp, 0.0)

    return int(firstNewRating), int(secNewRating), int(thirdNewRating)
    

def ExpectedValue(rOld, rOpp):
    eVal = 0
    eVal = 1.0 / (1 + pow(10.0, -((rOld - rOpp) / 400.0)))
    return eVal

def NewScore(oldScore, expected, actual):
    newScore = 0
    newScore = oldScore + kVal * (actual - expected)
    return newScore

def ConnectPlayers(sock):
    for p in players:
        #print("Key: " + p + ", Name: " + players[p])
        message = {"cmd":"playerConnect", "id":p, "name":players[p]["name"]}
        m = json.dumps(message)
        #print("Message to be dumped: " + m)
        sock.sendto(bytes(m, 'utf8'), sendToAddress)
        #print("Message sent")

if __name__ == "__main__":
    ipAddress = '52.15.65.92'
    port = 12345
    sendToAddress = (ipAddress, port)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    ConnectToServer(s)
    start_new_thread(heartbeat, (s,))
    start_new_thread(connectionLoop, (s,))
    ConnectPlayers(s)

    while True:
        time.sleep(1)