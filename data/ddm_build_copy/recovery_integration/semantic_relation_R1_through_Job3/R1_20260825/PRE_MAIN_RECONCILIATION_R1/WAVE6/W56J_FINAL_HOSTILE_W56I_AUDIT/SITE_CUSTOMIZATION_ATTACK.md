# sitecustomize and usercustomize attack

Detectable `sitecustomize.py` and `usercustomize.py` files were exposed from both the attacker cwd and PYTHONPATH-style location. Under `python3 -I -S`, marker count was 0. Neither startup hook executed.

