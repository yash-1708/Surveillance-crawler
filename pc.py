import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import threading
import pygame
import pyglet

def sending_thread(ip, port):
    pygame.init()
    page_width = 10
    page_height = 10
    size = page_width, page_height
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Paddle Pong")
    pygame.display.update()
    clock = pyglet.clock.Clock()
    clock.set_fps_limit(60)
    HOST = ip
    PORT = port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST, PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    conn, address = s.accept()
    print("Sent")
    while True:
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print("W")
                    conn.sendall("W".encode())
                elif event.key == pygame.K_s:
                    conn.sendall("S".encode())
                elif event.key == pygame.K_a:
                    conn.sendall("A".encode())
                elif event.key == pygame.K_d:
                    conn.sendall("D".encode())
                elif event.key == pygame.K_SPACE:
                    pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    conn.sendall("w".encode())
                elif event.key == pygame.K_s:
                    conn.sendall("s".encode())
                elif event.key == pygame.K_a:
                    conn.sendall("a".encode())
                elif event.key == pygame.K_d:
                    conn.sendall("d".encode())

def receiving_thread(ip, port):

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((ip, port))

    data = b''
    payload_size = struct.calcsize("L")
    print(type(data), payload_size, data)
    while True:
        while len(data) < payload_size:
            data += clientsocket.recv(4096)
            print(data)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += clientsocket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        ###

        frame \
            = pickle.loads(frame_data)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


t1 = threading.Thread(target=sending_thread, args=('192.168.43.110', 8089))
t2 = threading.Thread(target=receiving_thread, args=('192.168.43.5', 8089))

t2.start()
t1.start()