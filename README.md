<h1 align="center">Salut 👋, moi c’est ** Tadzo Morel **</h1>

\
<p align="center">
  Développeur backend passionné, je construis des applications  avec <strong>Java</strong> (Spring Boot) , pour la gestion bancaire, restaurant, de stocks, etc.
</p>

---

![Développeur qui code](https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif)


<img src="https://github-profile-trophy.vercel.app/?username=tadzo-morel" alt="GitHub Trophies">
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=tadzo-morel&layout=compact" alt="Top Languages">
---

##  Technologies & outils

<p align="left">
  <img src="https://img.shields.io/badge/Java-007396?style=for-the-badge&logo=java&logoColor=white" alt="Java"/>
  <img src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white" alt="Spring Boot"/>
  <img src="https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white" alt="PHP"/>
  <img src="https://img.shields.io/badge/MVC-000000?style=for-the-badge" alt="MVC"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS"/>
   <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"/>
  <img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman"/>
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/Haskell-5E5086?style=for-the-badge&logo=haskell&logoColor=white" alt="Haskell"/>
  <img src="https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=white" alt="C"/>
  <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" alt="C++"/>
  <img src="https://img.shields.io/badge/Visual_Studio-5C2D91?style=for-the-badge&logo=visual-studio&logoColor=white" alt="Visual Studio"/>
  <img src="https://img.shields.io/badge/Eclipse-2C2255?style=for-the-badge&logo=eclipse&logoColor=white" alt="Eclipse"/>
</p>
---

##  Statistiques GitHub

<p align="left">
  <img src="https://github-readme-stats.vercel.app/api?username=tadzo-morel&show_icons=true&theme=tokyonight" alt="GitHub Stats"/>
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=tadzo-morel&theme=tokyonight" alt="GitHub Streak"/>
</p>

---

##  Projets épinglés

- **etudiant** – Application de gestion d’étudiants (PHP).
- **gestion_stock** – Gestion des stocks en Java (MVC).
- **GestionCalculatriceBasique** – Calculatrice basique en Java.
- **GestionDesproduits** – Application Java (MVC) de gestion de produits.
- **GestionHopital2** – Système de gestion hospitalière en Java.
- **gestion_resto** – Gestion de restaurant en Java.
-  Nb: il se peut qu'il y est des modifications

---

##  En cours d’apprentissage

- Architecture microservices
- Tests unitaires (JUnit, Mockito)
- CI/CD (GitHub Actions)
- Fluter,bootStrap,pyton,angula

---
package com.example.tonprojet; // Mets ici le nom de ton package

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

import java.util.ArrayList;
import java.util.Random;

public class SnakeView extends SurfaceView implements Runnable {
    private Thread thread;
    private boolean isPlaying;
    private Paint paint;
    private ArrayList<Point> snake;
    private Point food;
    private int direction = 0; // 0=up, 1=right, 2=down, 3=left
    private int blockSize = 50;
    private int screenWidth, screenHeight;
    private Random random;

    public SnakeView(Context context) {
        super(context);
        getHolder().addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                screenWidth = getWidth();
                screenHeight = getHeight();
            }
            @Override public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {}
            @Override public void surfaceDestroyed(SurfaceHolder holder) {}
        });
        paint = new Paint();
        snake = new ArrayList<>();
        snake.add(new Point(5, 5));
        random = new Random();
        spawnFood();
    }

    @Override
    public void run() {
        while (isPlaying) {
            update();
            draw();
            control();
        }
    }

    private void update() {
        Point head = new Point(snake.get(0));
        switch (direction) {
            case 0: head.y -= 1; break;
            case 1: head.x += 1; break;
            case 2: head.y += 1; break;
            case 3: head.x -= 1; break;
        }

        // Collision mur
        if (head.x < 0 || head.x * blockSize >= screenWidth ||
            head.y < 0 || head.y * blockSize >= screenHeight) {
            resetGame();
            return;
        }

        // Collision avec soi-même
        for (Point p : snake) {
            if (p.equals(head)) {
                resetGame();
                return;
            }
        }

        snake.add(0, head);

        // Mange la nourriture
        if (head.equals(food)) {
            spawnFood();
        } else {
            snake.remove(snake.size() - 1);
        }
    }

    private void draw() {
        if (getHolder().getSurface().isValid()) {
            Canvas canvas = getHolder().lockCanvas();
            canvas.drawColor(Color.BLACK);

            paint.setColor(Color.GREEN);
            for (Point p : snake) {
                canvas.drawRect(p.x * blockSize, p.y * blockSize, (p.x + 1) * blockSize, (p.y + 1) * blockSize, paint);
            }

            paint.setColor(Color.RED);
            canvas.drawRect(food.x * blockSize, food.y * blockSize, (food.x + 1) * blockSize, (food.y + 1) * blockSize, paint);

            getHolder().unlockCanvasAndPost(canvas);
        }
    }

    private void spawnFood() {
        int maxX = screenWidth / blockSize;
        int maxY = screenHeight / blockSize;
        food = new Point(random.nextInt(maxX), random.nextInt(maxY));
    }

    private void resetGame() {
        snake.clear();
        snake.add(new Point(5, 5));
        direction = 0;
        spawnFood();
    }

    private void control() {
        try {
            Thread.sleep(150);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void pause() {
        isPlaying = false;
        try {
            if (thread != null) thread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void resume() {
        isPlaying = true;
        thread = new Thread(this);
        thread.start();
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (event.getAction() == MotionEvent.ACTION_DOWN) {
            float x = event.getX();
            float y = event.getY();
            Point head = snake.get(0);

            if (direction % 2 == 0) { // up ou down
                if (x > head.x * blockSize) direction = 1;
                else direction = 3;
            } else { // right ou left
                if (y > head.y * blockSize) direction = 2;
                else direction = 0;
            }
        }
        return true;
    }
}
##  Contact

Tu souhaites collaborer ou discuter d’un projet ?  
- **Email** : moreltadzo@gmail.com  
- **GitHub** : [tadzo-morel](https://github.com/tadzo-morel)  
- **LinkedIn**:https://www.linkedin.com/in/morel-aime-tadzo-9472012ab?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app  

<p align="center">
  Merci de visiter mon profil ! 🌟
</p>
