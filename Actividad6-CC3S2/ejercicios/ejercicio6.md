# Ejercicio 6: Cherry-pick y Git Stash
## 1. Cherry-pick
Commit a aplicar: aca7a8e

## 2. Git Stash
On branch feature/cherry-pick
You are currently cherry-picking commit aca7a8e.
  (all conflicts fixed: run "git cherry-pick --continue")
  (use "git cherry-pick --skip" to skip this patch)
  (use "git cherry-pick --abort" to cancel the cherry-pick operation)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   ../README.md
	modified:   ../logs/cherry-pick.txt
	modified:   ../logs/init-status.txt
	modified:   ../main.py
	modified:   ../../README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	./
	../logs/revert.txt

no changes added to commit (use "git add" and/or "git commit -a")

### Guardando cambios con stash
Cambios guardados temporalmente

### Estado después de stash
On branch feature/cherry-pick
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	./
	../logs/revert.txt

nothing added to commit but untracked files present (use "git add" to track)

### Cambios recuperados con stash pop
