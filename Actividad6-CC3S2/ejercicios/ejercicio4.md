# Ejercicio 4: git reset y git restore
## 1. Antes de git reset
b186c40 Introduce cambio para restablecer
aca7a8e Corregir error en funcionalidad de rollback
1a0933b correcciones y evidencias

## 2. Después de git reset --soft HEAD~1
El commit fue deshecho pero los cambios permanecen en staging
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   ../main.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   ../README.md
	modified:   ../logs/init-status.txt
	modified:   ../../README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	./
	../logs/revert.txt

## 3. Uso de git restore
Cambios no confirmados revertidos con: git restore <archivo>
