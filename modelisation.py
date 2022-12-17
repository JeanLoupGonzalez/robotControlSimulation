# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 14:21:09 2022

@author: larix
"""

import numpy as np
import matplotlib.pyplot as plt

""" Attributs de la classe Modelisation:

    CALCUL DE LA TRAJECTOIRE
        pointA et pointB : points donnés en entrée pour tous les calculs au format [x,y,z]
        longueurAB : norme du vecteur AB
        Vmax : vitesse max donnée par en entrée aussi 
        s(t) = [st], s'(t) = [sdt], s"(t) = [sddt] = paramètres modélisation la longueur distance parcorue ainsi que la vitesse et l'acceleration respectives
        tf, tc : temps final et temps de commutation
        coord_xyz , vit_xyz , accel_xyz : les coordonnes x,y,z de tous le points de la trajectoire entre les points A et B (la même chose pour la vitesse et l'acceleration')
        le grand X demandé est P ici : P = (x(t),y(t),z(t))

    CALCUL MGI
        inputs : (x,y,z,theta) -> (x,y,z) sont les vecteurs donnés par la modelisation de la trajectoire et theta est donée en entrée
        l1,l2,l3,l4,l5,h1,h2  -> parametres du robot qui peuvent être changés
        *le mgi donne 2 solutions pour chaque point :
            q1_p, q2_p, q3 et q4_p sont les solutions (1) de tous les points de la trajectoire
            q1_n, q2_n, q3 et q4_n sont les solutions (2) de tous les points de la trajectoire


    CALCUL MDI 
        on calcul les vecteurs q1(t)' = q1_point , q2(t)' = q2_point , q3(t)' = q3_point , q4(t)' = q4_point à partir d'une solution Q choisie ((1) ou (2))
"""


class Modelisation:

    # initialisation de tous les attributs utilisant numpy
    def __init__(self):
        self.taille = 100000  # combien de points on prends entre 0 et tf s

        # parametre pour la trajectoire
        self.pointA = []
        self.pointB = []
        self.st = np.array([])
        self.sdt = np.array([])
        self.sddt = np.array([])

        # parametre pour le mgi

        # parametres pour le mdi
        self.q1_point = np.array([])
        self.q2_point = np.array([])
        self.q3_point = np.array([])
        self.q4_point = np.array([])

    def setInputs(self, pa, pb, theta, vmax=10):
        # parametres pour la trajectoire

        self.pointA = pa
        self.pointB = pb
        self.vmax = vmax
        self.longueurAB = np.linalg.norm(np.array(self.pointB) - np.array(self.pointA))

        # initialisation du temps t, tf et tv
        self.tf = 2 * self.longueurAB / self.vmax  # Vmoy = (tf*Vmax/2)/tf
        self.tv = self.tf / 2
        self.t = np.linspace(0, self.tf, self.taille)

        # initialisation de theta
        self.theta = theta * np.ones(self.taille)

        # on relance tous les calculs a partir des nouvelles valeurs
        self.calculS()
        self.calculXYZ()
        self.calculMGI()
        self.calculMDI()

    def setParametres(self, L1, L2, L3, L4, L5, H1, H2):
        self.l1 = L1 * np.ones(self.taille)
        self.l2 = L2 * np.ones(self.taille)
        self.l3 = L3 * np.ones(self.taille)
        self.l4 = L4 * np.ones(self.taille)
        self.l5 = L5 * np.ones(self.taille)
        self.h1 = H1 * np.ones(self.taille)
        self.h2 = H2 * np.ones(self.taille)

    """CALCULS"""

    def calculS(self):
        # CALCUL DE s(t)

        # dans un premier temps on calcule s(t) pour 0<t<tv
        s1 = np.array(self.vmax * self.t[self.t <= self.tv] ** 2 / (2 * self.tv))

        # après on calcule s(t) pour tv<t<tf
        s2 = np.array(self.vmax * (
                    -(self.t[self.t > self.tv] ** 2) / 2 + self.tf * self.t[self.t > self.tv] - self.tf ** 2 / 2) / (
                                  self.tf - self.tv))  # il faut ajouter la dernière valeur de s1
        s2 = s2 + 2 * s1[-1]
        self.st = np.concatenate((s1, s2))

        # CALCUL DE s'(t)
        v1 = np.array(self.vmax * self.t[self.t <= self.tv] / self.tv)
        v2 = np.array(
            -self.vmax * self.t[self.t > self.tv] / (self.tf - self.tv) + self.vmax * self.tf / (self.tf - self.tv))
        self.sdt = np.concatenate((v1, v2))

        # CALCUL DE s"(t)
        a1 = np.ones(len(self.t[self.t <= self.tv])) * (self.vmax / self.tv)
        a2 = np.ones(len(self.t[self.t > self.tv])) * (-self.vmax / (self.tf - self.tv))
        self.sddt = np.concatenate((a1, a2))

    def calculXYZ(self):
        # CALCUL DE x(t),y(t),z(t)
        self.x = self.pointA[0] * np.ones(self.taille) + (self.pointB[0] - self.pointA[0]) * self.st / self.longueurAB
        self.y = self.pointA[1] * np.ones(self.taille) + (self.pointB[1] - self.pointA[1]) * self.st / self.longueurAB
        self.z = self.pointA[2] * np.ones(self.taille) + (self.pointB[2] - self.pointA[2]) * self.st / self.longueurAB

        # CALCUL DE x'(t),y'(t),z'(t)
        self.dx = (self.pointB[0] - self.pointA[0]) * self.sdt / self.longueurAB
        self.dy = (self.pointB[1] - self.pointA[1]) * self.sdt / self.longueurAB
        self.dz = (self.pointB[2] - self.pointA[2]) * self.sdt / self.longueurAB

        # CALCUL DE x"(t),y"(t),z"(t)
        self.ddx = (self.pointB[0] - self.pointA[0]) * self.sddt / self.longueurAB
        self.ddy = (self.pointB[1] - self.pointA[1]) * self.sddt / self.longueurAB
        self.ddz = (self.pointB[2] - self.pointA[2]) * self.sddt / self.longueurAB

    def calculMGI(self):
        # simplification d'écriture pour les calculs
        x = self.x
        y = self.y
        z = self.z
        costheta = np.cos(self.theta)
        sintheta = np.sin(self.theta)
        C1 = x - self.l5 * costheta - self.l1
        C2 = y - self.l5 * sintheta
        C3 = self.l3 + self.l4

        # calcul de q2 -> 2 solutions possibles
        # q1 et q4 ont dépendent de q2 donc 2 solutions possible pour chaque variable

        # on commence par calculer q2 -> on a besoin alors de cos(q2) et sin(q2) = sqrt(1 - cos(q2)²) ces qui nous donne 2 résultats possible : un positif et un négatif
        cosq2 = (np.square(C1) + np.square(C2) - np.square(self.l2) - np.square(C3)) / (2 * self.l2 * (C3))
        sinq2 = np.ones(self.taille) - np.square(cosq2)

        B1 = self.l2 + (C3) * cosq2

        # calcul de q3 -> 1 solution
        self.q3 = z - self.h1 - self.h2

        # SOLUTION (1) pour q1(t), q2(t) et q4(t)
        sinq2pos = np.sqrt(sinq2)
        B2pos = (C3) * sinq2pos  # simplification
        self.q2_p = np.arctan2(sinq2pos, cosq2)

        cosq1pos = (B1 * C1 + B2pos * C2) / (np.square(B1) + np.square((B2pos)))  # simplification
        sinq1pos = (B1 * C2 - B2pos * C1) / (np.square(B1) + np.square((B2pos)))  # simplification
        self.q1_p = np.arctan2(sinq1pos, cosq1pos)

        self.q4_p = self.theta - self.q1_p - self.q2_p

        # SOLUTION (2)  pour q1(t), q2(t) et q4(t)
        sinq2neg = -np.sqrt(sinq2)
        B2neg = (C3) * sinq2neg  # simplification
        self.q2_n = np.arctan2(sinq2neg, cosq2)

        cosq1neg = (B1 * C1 + B2neg * C2) / (np.square(B1) + np.square((B2neg)))  # simplification
        sinq1neg = (B1 * C2 - B2neg * C1) / (np.square(B1) + np.square((B2neg)))  # simplification
        self.q1_n = np.arctan2(sinq1neg, cosq1neg)

        self.q4_n = self.theta - self.q1_n - self.q2_n

    def calculMDI(self):
        # Q pour solution (1)

        c1 = np.cos(self.q1_p)
        s1 = np.sin(self.q1_p)

        c2 = np.cos(self.q2_p)
        s2 = np.sin(self.q2_p)

        c12 = c1 * c2 - s1 * s2
        s12 = c1 * s2 + s1 * c2

        for i in range(self.taille):
            # Ici on donne directement la formule de la Jacobienne mais la démarche
            # pour l'avoir est detaillée dans le rapport

            v1 = [c12[i] * self.l2[i] * s2[i] - s12[i] * (self.l1[i] * c2[i] + self.l3[i] + self.l4[i]),
                  -s12[i] * (self.l3[i] - self.l4[i]), s12[i] * self.l4[i], 2 * self.l4[i] * s12[i]]
            v2 = [s12[i] * self.l1[i] * s2[i] + c12[i] * (self.l1[i] * c2[i] + self.l3[i] + self.l4[i]),
                  c12[i] * (self.l3[i] - self.l4[i]), -c12[i] * self.l4[i], -2 * self.l4[i] * c12[i]]
            J = np.array([v1, v2, [0, 0, 1, 0], [1, 1, 1, 1]])

            X = [[self.x[i]], [self.y[i]], [self.z[i]], [1]]
            q_point = np.dot(np.linalg.inv(J), X)

            self.q1_point = np.append(self.q1_point, q_point[0])
            self.q2_point = np.append(self.q2_point, q_point[1])
            self.q3_point = np.append(self.q3_point, q_point[2])
            self.q4_point = np.append(self.q4_point, q_point[3])

    """AFFICHAGES"""

    def affichageS(self):
        fig, axes = plt.subplots(1, 3, figsize=(17, 5))
        axes[0].set_title('s(t)')
        axes[0].plot(self.t, self.st)
        axes[0].axvline(x=self.tv, ymin=0, ymax=11, color='red', alpha=0.5, linestyle='--', linewidth=4,
                        label=r'$T commutation$')
        # axes[0].annotate('T commutation', xy = (self.tv, 0), xytext = (self.tv+0.1*self.tf, self.tv),
        # arrowprops = {'facecolor': 'orange', 'shrink': 0.1})
        axes[0].legend()

        axes[1].set_title('s\'(t)')
        axes[1].plot(self.t, self.sdt)
        axes[1].axvline(x=self.tv, ymin=0, ymax=11, color='red', alpha=0.5, linestyle='--', linewidth=4)

        axes[2].set_title('s"(t)')
        axes[2].plot(self.t, self.sddt)
        plt.show()

    def affichageXYZ(self):
        fig, axes = plt.subplots(1, 3, figsize=(17, 5))

        axes[0].set_title('trajectoire en fonction du temps')
        axes[0].plot(self.t, self.x, label=r'$x(t)$')
        axes[0].plot(self.t, self.y, label=r'$y(t)$')
        axes[0].plot(self.t, self.z, label=r'$z(t)$')
        axes[0].legend()

        axes[1].set_title('vitesse(t)')
        axes[1].plot(self.t, self.dx, label=r'$x\'(t)$')
        axes[1].plot(self.t, self.dy, label=r'$y\'(t)$')
        axes[1].plot(self.t, self.dz, label=r'$z\'(t)$')
        axes[1].legend()

        axes[2].set_title('acceleration(t)')
        axes[2].plot(self.t, self.ddx, label=r'$x"(t)$')
        axes[2].plot(self.t, self.ddy, label=r'$y"(t)$')
        axes[2].plot(self.t, self.ddz, label=r'$z"(t)$')
        axes[2].legend()

        plt.show()

    def affichageP(self):
        plt.figure(figsize=(30, 7))
        ax = plt.axes(projection='3d')
        ax.plot3D(self.x, self.y, self.z)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('X(s)')

        plt.show()

    # affichage de la vitesse du point O5 dans la base 0
    def affichageVit(self):
        # pour chaque t, on calcule la racine de x(t)**2 + y(t)**2 + z(t)**2
        vit = np.sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)
        plt.plot(self.t, vit)

        plt.title("Vitesse du point O5 dans R0")
        plt.xlabel('t')
        plt.ylabel('VO5(t)')

        plt.show()

    def affichageQ(self):
        # on utilise ici la solution (1) pour l'affichage -> plus précis
        fig, axes = plt.subplots(2, 2, figsize=(20, 10))

        axes[0][0].set_title('solution1 de q1(t) , q1\'(t)')
        axes[0][0].plot(self.t, self.q1_p, label=r'$q1(t)$')
        axes[0][0].axvline(x=self.tv, ymin=0, ymax=11, color='magenta', alpha=0.5, linestyle='--', linewidth=4,
                           label=r'$T commutation$')
        axes[0][0].axhline(y=self.theta[0], xmin=0, xmax=self.taille, color='black', alpha=0.5, linestyle='-',
                           linewidth=4, label=r'$\theta$')
        # axes[0][0].plot(self.t,self.q1_point,label = r'$q1\'(t)$')

        axes[0][0].legend()

        axes[0][1].set_title('solution1 de q2(t) , q1\'(t)')
        axes[0][1].plot(self.t, self.q2_p, color='green', label=r'$q2(t)$')
        axes[0][1].axvline(x=self.tv, ymin=0, ymax=11, color='magenta', alpha=0.5, linestyle='--', linewidth=4,
                           label=r'$T commutation$')
        axes[0][1].axhline(y=self.theta[0], xmin=0, xmax=self.taille, color='black', alpha=0.5, linestyle='-',
                           linewidth=4, label=r'$\Theta$')
        # axes[0][1].plot(self.t,self.q2_point,label = r'$q2\'(t)$')

        axes[0][1].legend()

        axes[1][0].set_title('solution1 de q3(t) ,  q3\'(t)')
        axes[1][0].plot(self.t, self.q3, color='orange', label=r'$q3(t)$')
        axes[1][0].axvline(x=self.tv, ymin=0, ymax=11, color='magenta', alpha=0.5, linestyle='--', linewidth=4,
                           label=r'$T commutation$')
        # axes[1][0].plot(self.t,self.q3_point,label = r'$q3\'(t)$')

        axes[1][0].legend()

        axes[1][1].set_title('solution1 de q4(t) , q4\'(t)')
        axes[1][1].plot(self.t, self.q4_p, color='red', label=r'$q4(t)$')
        # axes[1][1].plot(self.t,self.q4_point,label = r'$q4\'(t)$')
        axes[1][1].axvline(x=self.tv, ymin=0, ymax=11, color='magenta', alpha=0.5, linestyle='--', linewidth=4,
                           label=r'$T commutation$')
        axes[1][1].axhline(y=self.theta[0], xmin=0, xmax=self.taille, color='black', alpha=0.5, linestyle='-',
                           linewidth=4, label=r'$\Theta$')

        axes[1][1].legend()

        plt.show()

    def dessinerRobot(self):
        # dessin de l'état initial du robot
        OX0, OY0, OZ0 = (0, 0, 0)
        OX1, OY1, OZ1 = (self.l1[0], 0, self.h1[0])
        OX2, OY2, OZ2 = (OX1 + (self.l2[0] * np.cos(self.q1_p[0])), OY1 + (self.l2[0] * np.sin(self.q1_p[0])), OZ1)
        OX3, OY3, OZ3 = (OX2 + (self.l3[0] * np.cos(self.q2_p[0])), OY2 + (self.l3[0] * np.sin(self.q2_p[0])), OZ1)
        OX4, OY4, OZ4 = (OX3 + self.l4[0], OY3, OZ3 + self.q3[0])
        OX5, OY5, OZ5 = (OX4 + (self.l5[0] * np.cos(self.q4_p[0])), OY4 + (self.l5[0] * np.sin(self.q4_p[0])), OZ4)

        X = [OX0, OX1, OX2, OX3, OX4, OX5]
        Y = [OY0, OY1, OY2, OY3, OY4, OY5]
        Z = [OZ0, OZ1, OZ2, OZ3, OZ4, OZ5]

        plt.plot(X, Z, color="green", lw=10, alpha=0.5, marker="o", markersize=20, mfc="red")
        plt.axis('equal')
        plt.axis('off')
        plt.scatter(OX5, OZ5, marker="$\in$", s=800, c="black", zorder=3)

        plt.show()

        # tout afficher

    def affichage(self):
        self.affichageS()
        self.affichageXYZ()
        self.affichageP()
        self.affichageVit()
        self.affichageQ()
