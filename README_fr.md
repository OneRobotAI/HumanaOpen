# HumanaOpen

[English](README.md) | [中文](README_zh.md) | [Français](README_fr.md) | [한국어](README_ko.md)

**Robot semi-humoïde open source — 7 DOF double bras, différentiel, et vérin de levage.**

Construit sur [LeRobot](https://github.com/huggingface/lerobot) et
[open-arms-mini](https://github.com/TheRobotStudio/open-arms-mini).

## Matériel

| Sous-système | Moteurs | Modèle |
|-----------|--------|-------|
| Bras suiveur gauche | 8 (7-DOF + pince) | ST3215 C018 (1:345) |
| Bras suiveur droit | 8 (7-DOF + pince) | ST3215 C018 (1:345) |
| Tête (pan/tilt) | 2 | ST3215 C018 (1:345) |
| Levage (vis sans fin) | 1 | ST3250 (entraînement direct, sans courroie) |
| Base à roues différentielles | 2 | ST3215 C018 (1:345) |
| Bras leaders (téléop) | 2 × 8 | STS3215 C046 (1:147) |

> **Convention gauche/droite** : Définie depuis le référentiel du robot.
> Debout derrière le robot en regardant dans la même direction, le bras à votre
> gauche est le **bras gauche** (`port1`), celui à votre droite est le
> **bras droit** (`port2`). Le câblage détermine quel bras physique est lequel ;
> le logiciel mappe simplement `left_arm_*` → `port1` et `right_arm_*` → `port2`.

## Logiciel

```
lerobot_robot_humanaopen/
├── __init__.py              # Exports du package
├── config_humanaopen.py     # HumanaOpenConfig, configs host/client
├── humanaopen.py            # Classe Robot HumanaOpen (suiveur)
├── lift_axis.py             # Axe de levage avec homing par détection de blocage
├── leader.py                # Téléopérateur leader (simple/bimanuel)
├── humanaopen_host.py       # Hôte ZMQ (côté robot, mode double machine)
└── humanaopen_client.py     # Client ZMQ (côté téléop)
examples/
├── record_data.py              # Collecte de données (API Python, tous paramètres)
├── eval_data.py                # Inférence (déploiement politique ACT)
├── single_machine.py           # Opération mono-machine
├── teleop_keyboard.py          # Téléopération clavier via ZMQ
├── teleop_leader_to_follower.py  # Téléop corps entier : bras leaders + clavier
├── calibrate_follower.py       # Calibration complète suiveur (bras+tête+roues+levage)
├── calibrate_leader.py         # Calibration bras leader (open-arms-mini)
├── diagnose_teleop.py          # Diagnostic direction articulations téléop
├── test_base_keyboard.py       # Test clavier base uniquement (sans levage/bras)
├── test_lift_only.py           # Test axe de levage (homing + montée/descente)
└── check_phase.py              # Vérifier unité de vitesse servo (Phase BIT2)
```

## Matériel

```
hardware/
├── README.md               # Aperçu du matériel (guide des répertoires)
├── BOM/bom.md              # Liste de pièces — composants, spécifications, approvisionnement
├── assembly/assembly.md    # Instructions d'assemblage pas à pas
├── cad/
│   ├── fusion360/          # Conceptions sources Fusion 360 (.f3d)
│   └── step/               # Exports STEP (.step/.stp)
├── stl/                    # Fichiers d'impression 3D prêts à imprimer (.stl)
├── urdf/                   # Description du robot (RViz / Gazebo / simulation)
│   └── humanaopen.urdf     # (meshes/ contient les maillages STL référencés)
└── electronics/wiring.md   # Câblage / disposition électronique et alimentation
```

### Outils de diagnostic et réglage

| Script | Objectif |
|--------|---------|
| `diag_head_tilt_limits.py` | Sonde plage mécanique inclinaison tête (avant/après déblocage) |
| `diag_head_tilt_range.py` | Diagnostic plage d'inclinaison tête |
| `diag_regression.py` | Test de régression (levage + caméra + séquence téléop) |
| `diag_st3250_speed.py` | Profil vitesse moteur ST3250 (Phase BIT2=1) |
| `diag_follower_gripper.py` | Diagnostic articulation pince |
| `recover_lift_ping.py` | Ping communication moteur de levage |
| `speed_test_bit2_0.py` | Vérification vitesse BIT2=0 |
| `switch_phase_bit2.py` | Basculer registre Phase BIT2 ST3250 |
```

## Démarrage rapide

```bash
# 1. Créer un environnement conda
conda create -n humanaopen python=3.12
conda activate humanaopen

# 2. Installer LeRobot (dépendance requise)
pip install "lerobot[dataset,training,feetech,viz,transformers-dep,hardware,smolvla]"

# 3. Installer HumanaOpen (editable)
cd /chemin/vers/HumanaOpen
pip install -e . --no-deps


# Required: SOCKS proxy support (for HuggingFace upload behind proxy)
pip install httpx[socks] num2words


# Optionnel : installer les dépendances SmolVLA (transformers, num2words)
pip install -e ".[smolvla]" 2>/dev/null || pip install transformers>=4.48 num2words

# Optionnel : GPU avec CUDA 12.8+ (Blackwell / RTX 5060+)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# 4. Vérifier l'installation
python -c "from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig; print('✅ OK')"

# 5. Opération mono-machine
python -c "
from lerobot_robot_humanaopen import HumanaOpen, HumanaOpenConfig
config = HumanaOpenConfig(port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None, cameras={})
robot = HumanaOpen(config)
robot.connect(calibrate=False)
print(robot.get_observation().keys())
"

# 6. Mode ZMQ double machine (exécuter sur le robot)
# Démarrer le Host (avec caméras). Téléop pure sans image ? Utilisez cameras={} à la place.
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={
        'head':         OpenCVCameraConfig(index_or_path='/dev/video0', fps=30, width=640, height=480, fourcc='MJPG'),  # ajustez /dev/videoN selon la sortie de lerobot-find-cameras
        'left_wrist':   OpenCVCameraConfig(index_or_path='/dev/video2', fps=30, width=640, height=480, fourcc='MJPG'),  # ajustez /dev/videoN selon la sortie de lerobot-find-cameras
        'right_wrist':  OpenCVCameraConfig(index_or_path='/dev/video4', fps=30, width=640, height=480, fourcc='MJPG'),
                # 'chest': OpenCVCameraConfig(index_or_path='/dev/video6', fps=30, width=640, height=480, fourcc='MJPG'),  # 4e camera — décommenter pour activer
    },
    wheel_dir_signs={'base_left_wheel': -1, 'base_right_wheel': 1}
)).run()
"
```

## Déploiement double machine

Pour le déploiement, le matériel se connecte à une carte embarquée (Jetson ou Raspberry Pi),
l'inférence s'exécute sur une machine GPU séparée. Communication via ZMQ.
Voir [Dual-Machine Deployment](README.md#dual-machine-deployment) pour le guide complet.

Architecture : Machine dev (GPU) ←→ Jetson/RPi (Host), ports ZMQ 5555/5556.

### Raspberry Pi (Host uniquement)
```bash
conda create -n humanaopen python=3.12
conda activate humanaopen

# Host dependencies (lightweight — no torch/transformers needed)
pip install pyzmq feetech-servo-sdk
cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps
# Démarrer le Host (avec caméras). Téléop pure sans image ? Utilisez cameras={} à la place.
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={
        'head':         OpenCVCameraConfig(index_or_path='/dev/video0', fps=30, width=640, height=480, fourcc='MJPG'),  # ajustez /dev/videoN selon la sortie de lerobot-find-cameras
        'left_wrist':   OpenCVCameraConfig(index_or_path='/dev/video2', fps=30, width=640, height=480, fourcc='MJPG'),  # ajustez /dev/videoN selon la sortie de lerobot-find-cameras
        'right_wrist':  OpenCVCameraConfig(index_or_path='/dev/video4', fps=30, width=640, height=480, fourcc='MJPG'),
                # 'chest': OpenCVCameraConfig(index_or_path='/dev/video6', fps=30, width=640, height=480, fourcc='MJPG'),  # 4e camera — décommenter pour activer
    },
    wheel_dir_signs={'base_left_wheel': -1, 'base_right_wheel': 1}
)).run()
"
```

### Jetson (Host + inférence locale optionnelle)
```bash
# Même installation que Raspberry Pi — Host n'a pas besoin de torch/transformers
conda create -n humanaopen python=3.12
conda activate humanaopen

pip install pyzmq feetech-servo-sdk
# conda install -y ffmpeg=7.1.1 -c conda-forge  # optionnel

cd ~/ && git clone https://github.com/OneRobotAI/HumanaOpen.git
cd HumanaOpen && pip3 install -e . --no-deps
# Démarrer le Host (avec caméras). Téléop pure sans image ? Utilisez cameras={} à la place.
python3 -c "
from lerobot_robot_humanaopen.humanaopen_host import HumanaOpenHost
from lerobot_robot_humanaopen import HumanaOpenConfig
from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig

HumanaOpenHost(HumanaOpenConfig(
    port1='/dev/ttyACM0', port2='/dev/ttyACM1', port3=None,
    cameras={
        'head':         OpenCVCameraConfig(index_or_path='/dev/video0', fps=30, width=640, height=480, fourcc='MJPG'),  # ajustez /dev/videoN selon la sortie de lerobot-find-cameras
        'left_wrist':   OpenCVCameraConfig(index_or_path='/dev/video2', fps=30, width=640, height=480, fourcc='MJPG'),  # ajustez /dev/videoN selon la sortie de lerobot-find-cameras
        'right_wrist':  OpenCVCameraConfig(index_or_path='/dev/video4', fps=30, width=640, height=480, fourcc='MJPG'),
                # 'chest': OpenCVCameraConfig(index_or_path='/dev/video6', fps=30, width=640, height=480, fourcc='MJPG'),  # 4e camera — décommenter pour activer
    },
    wheel_dir_signs={'base_left_wheel': -1, 'base_right_wheel': 1}
)).run()
"
```

### Mode dual-machine (--remote_ip)

Tous les scripts (record, eval, teleop) supportent le mode dual-machine via `--remote_ip`.
Le mode single-machine (défaut) utilise le port série direct ; le mode dual ajoute ZMQ :

```bash
# Mode single-machine (défaut — pas de --remote_ip nécessaire)
python3 examples/record_data.py ...

# Mode dual-machine (ajouter --remote_ip)
python3 examples/record_data.py --remote_ip=192.168.1.100 ...
python3 examples/eval_data.py --remote_ip=192.168.1.100 ...
python3 examples/teleop_leader_to_follower.py --remote_ip=192.168.1.100 ...
```


### Exigences réseau
- Même LAN, ports 5555 et 5556 ouverts
- Bande passante : ~10 Mbps par caméra


### Performances

- Boucle de contrôle : 30Hz (lecture état + commande action)
- Capture image : 30fps (thread dédié — ne bloque pas le contrôle)
- Faible latence : la capture image est découplée de la boucle de contrôle
- Configurable : `image_fps_divider` (ratio boucle/image) et `max_loop_freq_hz` (fréquence contrôle) dans

### Direction des roues (double machine)

La roue gauche est montée en miroir ; utilisez `wheel_dir_signs={'base_left_wheel': -1, 'base_right_wheel': 1}`. C'est le défaut dans `HumanaOpenConfig`.

## Calibration

La calibration enregistre la plage min/max de chaque articulation. **Une seule fois nécessaire** —
les résultats sont sauvegardés et restaurés automatiquement à chaque connexion.

### Quand calibrer

- **Première installation** (requis)
- Après démontage/remontage des bras ou servos
- Après remplacement d'un servo moteur
- Après déblocage d'une nouvelle amplitude (ex: déblocage EPROM du tilt tête)

### Calibration du bras leader

```bash
python3 examples/calibrate_leader.py
```

Étapes (par bras) :
1. Bras pendant verticalement + pince fermée → `ENTER` (point zéro)
2. Déplacer chaque articulation sur toute sa course → `ENTER` (limites réelles)
3. Pince : fermer complètement → `ENTER`, ouvrir complètement → `ENTER`
4. Calibration sauvegardée automatiquement

> Les bras leaders doivent être alimentés en **7.4V** sur `/dev/ttyACM2` (gauche) et `/dev/ttyACM3` (droite).

Sauvegardé dans :
```
~/.cache/huggingface/lerobot/calibration/teleoperators/humanaopen_leader/
├── leader_left.json
└── leader_right.json
```

### Calibration du suiveur (bras + tête + roues + levage)

```bash
python3 examples/calibrate_follower.py
```

Étapes :
1. Bras gauche + tête : position zéro → `ENTER` ; parcourir toute la course → `ENTER`
2. Bras droit : position zéro → `ENTER` ; parcourir toute la course → `ENTER`
3. Auto : roues pleine plage + homing blocage du levage vers le bas

> Le suiveur doit être alimenté en **12V**. Le couple est relâché pendant la calibration — bras mobiles librement.

Sauvegardé dans :
```
~/.cache/huggingface/lerobot/calibration/robots/humanaopen/follower.json
```


## Téléopération

### Téléop corps entier (bras leaders + clavier)

`teleop_leader_to_follower.py` pilote les bras du suiveur depuis les bras leaders,
et la tête/base/levage depuis le clavier :

| Contrôle | Touches |
|---------|------|
| Bras | suivi des bras leaders (flips désactivés — direction vérifiée identique) |
| Tête | `w`/`s` hocher (haut/bas), `a`/`d` secouer (gauche/droite) |
| Base | `i`/`k` avant/arrière, `j`/`l` tourner, `n`/`m` vitesse (0.3x/0.6x/1.0x) |
| Levage | `u`/`h` monter/descendre (limité 3–200mm) |
| Quitter | `b` ou Ctrl+C |

```bash
# Par défaut : 3 caméras (head + left_wrist + right_wrist)
python3 examples/teleop_leader_to_follower.py

# Ajouter la 4ème caméra poitrine
python3 examples/teleop_leader_to_follower.py --chest-camera /dev/video6

# Mode double machine : Host sur le robot, téléop sur votre PC
python3 examples/teleop_leader_to_follower.py --remote_ip=192.168.1.100 --chest-camera /dev/video6

# Téléop uniquement, sans caméras
python3 examples/teleop_leader_to_follower.py --no-cameras
```

#### Modes d'affichage en direct

`teleop_leader_to_follower.py` prend en charge deux backends de visualisation.
Les images sont décodées une seule fois par la boucle de contrôle, puis
déléguées à un thread d'affichage en arrière-plan — la boucle de 30 Hz
n'est jamais bloquée.

| Option | Backend | Notes |
|--------|---------|-------|
| `--display=rerun` | [Rerun](https://rerun.io) fenêtre native | Fenêtre native du viewer Rerun. |
| `--display=foxglove` | [Foxglove Studio](https://foxglove.dev) WebSocket | Se connecte à `ws://127.0.0.1:8765`. Un layout est écrit dans `examples/humanoopen_foxglove.layout.json` (import une seule fois). **Recommandé** — latence la plus basse des deux. |

Omettez `--display` pour exécuter sans visualisation (headless).

```bash
# Foxglove (recommandé)
python3 examples/teleop_leader_to_follower.py --remote_ip=192.168.1.100 --display=foxglove

# Rerun
python3 examples/teleop_leader_to_follower.py --remote_ip=192.168.1.100 --display=rerun
```

> **Latence d'affichage** : Les deux backends ajoutent un délai de rendu
> fixe (≈1–1,5 s desktop / ≈2 s viewer natif) inhérent aux bibliothèques
> de visualisation. Les commandes d'action (bras) sont en temps réel ; le
> lag d'affichage n'affecte **pas** la qualité des données enregistrées —
> observation et action sont toujours synchronisées dans la même image.

Arguments caméra : `--cameras=head,left_wrist` (sous-ensemble), `--head-camera /dev/videoN`,
`--left-wrist-camera`, `--right-wrist-camera`, `--chest-camera` (chacun remplace le
chemin du périphérique ; passer un argument `--*-camera` ajoute automatiquement cette caméra).

### Périphériques caméra et fps (testés)

| Caméra | Périphérique | Format | FPS |
|--------|--------|--------|-----|
| head | /dev/video0 | MJPG | 30 |
| left_wrist | /dev/video2 | MJPG | 30 |
| right_wrist | /dev/video4 | MJPG | 30 |
| chest | /dev/video6 | MJPG | 30 |

> **Ajustement FPS** : Vérifiez les capacités réelles avec
> `v4l2-ctl -d /dev/videoN --list-formats-ext`, puis mettez à jour la valeur `fps` dans les scripts.
> Définir un fps non supporté provoquera une erreur de connexion au démarrage.



### Axe de levage — persistance du zéro (免归零)

Le levage utilise un encodeur 12 bits simple tour (4096 ticks/tour) entraînant une vis sans fin
(25 tours = 200mm). La position absolue est suivie en logiciel via un suivi multi-tours.
Comme la vis est autobloquante, la position mécanique survit aux cycles d'alimentation —
la position zéro est donc persistée dans `~/.cache/humanaopen/lift_zero.json`
et restaurée à la prochaine connexion, **sans re-homing** :

- Première connexion : descend jusqu'en bas (détection de blocage), sauvegarde le zéro.
- Connexions suivantes : restaure la position absolue sauvegardée (aucun mouvement nécessaire).
- Si la position a changé (ex. levage déplacé manuellement), la restauration échoue et
  l'auto-homing s'exécute à la place.

Réglages du levage (testés) : `v_max=110` (raw), `kp_vel=10`, `home_down_speed=10` avec
Phase BIT2=0 (50 pas/s par unité raw). Vitesse max ≈ 8,7mm/s (200mm en ~23s).

### Accélération du levage (BIT2=0)

Le firmware ST3250 mappe `Goal_Velocity` avec Phase BIT2=1 à 1 pas/s par unité raw,
où raw > 1000 inverse la direction (onde triangulaire) — dangereux. Passer en Phase BIT2=0
change l'unité à 50 pas/s par unité raw, donc la pleine vitesse (5500 pas/s) correspond à raw 110,
entièrement dans la plage fiable. **Après le basculement, tous les paramètres de vitesse doivent
être divisés par 50** (`home_down_speed`, `kp_vel`, `v_max`). Outils :
`examples/switch_phase_bit2.py` (basculer), `examples/speed_test_bit2_0.py` (vérifier).

### Déblocage de la plage d'inclinaison de la tête

Le servo d'inclinaison de la tête avait des limites de position EPROM fixées à [1430, 2096] (~58°),
que le fichier de calibration a copiées — limitant l'inclinaison à -54°/+4°. Écrire
`Min=0 / Max=4095` débloque la plage mécanique [1367, 2242] (-61,6°/+17,1°) :
`examples/unlock_head_tilt.py --probe`. Après le déblocage, le fichier de calibration
(`~/.cache/huggingface/lerobot/calibration/robots/humanaopen/follower.json`) a été
mis à jour avec la plage réelle.

## Collecte de données

La CLI `lerobot-record` code en dur les types de robots officiels et rejette `humanaopen`
comme choix non reconnu. Utilisez le wrapper API Python `examples/record_data.py`
à la place — il expose les **mêmes noms de paramètres** que `lerobot-record` et affiche
la commande CLI équivalente au démarrage pour référence.

### 3 caméras (par défaut)

```bash
python3 examples/record_data.py \
    --robot.type=humanaopen \
    --robot.id=follower \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=None \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --robot.confirm_lift_after_home=true \
    --teleop.left_arm_port=/dev/ttyACM2 \
    --teleop.right_arm_port=/dev/ttyACM3 \
    --teleop.flip_joints='{"left": [], "right": []}' \
    --teleop.joint_remap='{}' \
    --dataset.repo_id=votre-nom/humanaopen_demo \
    --dataset.single_task="décrivez votre tâche" \
    --dataset.num_episodes=2 \
    --dataset.episode_time_s=15 \
    --dataset.reset_time_s=10 \
    --dataset.fps=30 \
    --dataset.push_to_hub=true
```

### 4 caméras (avec poitrine pour la navigation)

Identique à ci-dessus, mais remplacer le JSON `--robot.cameras` pour inclure chest :

```bash
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "chest": {"type": "opencv", "index_or_path": "/dev/video6", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
```

> **Note** : les noms de caméras doivent être cohérents entre enregistrement / entraînement / déploiement.

### Double machine (ZMQ) : Host sur le robot, enregistrement sur le PC

Quand le follower tourne sur le robot (avec ses propres caméras) et que les bras
leaders sont branchés sur le PC, enregistrez via ZMQ. **Démarrez le Host d'abord**,
puis lancez `record_data.py` sur le PC :

```bash
# 1) Sur le robot (Jetson ou Raspberry Pi, voir "Installation : Raspberry Pi / Jetson"
#    ci-dessus) — démarrez le Host et laissez-le tourner
#    (HumanaOpenHost(...).run() avec port1/port2 + les 3 caméras).

# 2) Sur votre PC — enregistrez (follower via ZMQ, leader via le ttyACM0/1 local)
python3 examples/record_data.py \
    --remote_ip=192.168.1.9 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --teleop.left_arm_port=/dev/ttyACM0 \
    --teleop.right_arm_port=/dev/ttyACM1 \
    --teleop.flip_joints='{"left": [], "right": []}' \
    --teleop.joint_remap='{}' \
    --dataset.repo_id=votre-nom/humanaopen_demo \
    --dataset.single_task="décrire votre tâche" \
    --dataset.num_episodes=2 \
    --dataset.episode_time_s=15 \
    --dataset.reset_time_s=10 \
    --dataset.fps=30 \
    --dataset.push_to_hub=true \
    --display=foxglove
```

- `--remote_ip` passe en mode double machine : le follower se connecte au Host via
  ZMQ (les `--robot.type/id/port1-3` ne sont **pas** nécessaires), les bras leaders
  utilisent les ports série locaux du PC.
- `--robot.cameras` est passé comme *schéma* (noms + résolutions) ; le Host possède
  les caméras physiques et diffuse les images via ZMQ.
- `--display=foxglove` (optionnel) diffuse caméras + état à l'application Foxglove
  sur le PC (connectez Studio à `ws://127.0.0.1:8765`).

### Contrôles pendant l'enregistrement

| Contrôle | Touches |
|---------|------|
| Bras | suivi des bras leaders (16 DOF) |
| Tête | `w`/`s` hocher, `a`/`d` secouer (2 DOF) |
| Base | `i`/`k` avant/arrière, `j`/`l` tourner (2 DOF, vitesse `n`/`m`) |
| Levage | `u`/`h` monter/descendre avec limites de sécurité (1 DOF, limité 3–200mm) |
| Enregistrer | `C` démarrer, `Q` quitter, `A` ré-enregistrer l'épisode |
| Confirmer | Après homing, maintenir `u`/`h` pour positionner, `ENTER` pour confirmer |

Le téléopérateur `--teleop.type=humanaopen_teleop` enregistre **tous les 21 DOF** — les
bras leaders (16 articulations) plus la tête/levage/base contrôlés au clavier (5 DOF). Les deux sont
sauvegardés dans le dataset pour l'entraînement ACT.

### Comportement du levage pendant l'enregistrement

- À la première connexion : le levage **descend jusqu'en bas** (détection de blocage), sauvegarde le zéro
  dans `~/.cache/humanaopen/lift_zero.json`.
- Aux connexions suivantes : le levage **restaure la position sauvegardée** (pas de homing nécessaire),
  sauf si la position a changé (poussée manuelle → échec de restauration → auto-home).
- Après le homing : maintenir `u`/`h` au clavier ajuste la hauteur avec limites de sécurité
  (3mm–200mm), `ENTER` pour confirmer et commencer l'enregistrement.

### Reprise / nettoyage des datasets

Si un répertoire de dataset existe déjà d'une exécution précédente, supprimez-le ou reprenez :

```bash
rm -rf ~/.cache/huggingface/lerobot/votre-nom/humanaopen_demo    # nouveau départ
# ou ajouter --dataset.resume=true à la commande record_data.py   # continuer depuis le dernier épisode
```

### Affichage en direct pendant l'enregistrement (optionnel)

Par défaut l'enregistrement tourne sans visualisation. Pour surveiller les
caméras et l'état en temps réel pendant la téléopération, ajoutez un drapeau :

```bash
# Visualiseur Rerun
python3 examples/record_data.py ... --display=rerun

# Application Foxglove (recommandé — latence plus basse, même backend que teleop)
python3 examples/record_data.py ... --display=foxglove
# connectez Foxglove Studio à ws://127.0.0.1:8765
```

> L'affichage est découplé de la boucle d'enregistrement, il ne perturbe jamais
> les trames `(observation, action)` enregistrées. Comme en teleop, le visualiseur
> ajoute ~1–1,5s de délai de rendu qui **n'affecte pas** la qualité des données.

## Entraînement

### ACT (action chunking transformer)

```bash
# Test rapide (2 épisodes)
lerobot-train \
    --policy.type=act \
    --policy.device=cuda \
    --policy.push_to_hub=true \
    --policy.repo_id=votre-nom/humanaopen_act_policy \
    --dataset.repo_id=votre-nom/humanaopen_act_demo \
    --output_dir=outputs/humanaopen_act_demo \
    --batch_size=3 \
    --steps=5

# Production (>50 épisodes)
lerobot-train \
    --policy.type=act \
    --policy.device=cuda \
    --policy.push_to_hub=true \
    --policy.repo_id=votre-nom/humanaopen_act_policy \
    --dataset.repo_id=votre-nom/humanaopen_act_demo \
    --output_dir=outputs/humanaopen_act_demo \
    --batch_size=32 \
    --steps=50000
```

### SmolVLA (modèle vision-langage-action)

SmolVLA nécessite l'instruction en langue de `--dataset.single_task` (utilisée pendant l'enregistrement).
Les poids VLM (~500M) sont téléchargés automatiquement depuis HuggingFace au premier lancement.

```bash
# Test rapide (2 épisodes)
lerobot-train \
    --policy.type=smolvla \
    --policy.device=cuda \
    --policy.push_to_hub=true \
    --policy.repo_id=votre-nom/humanaopen_smolvla_policy \
    --dataset.repo_id=votre-nom/humanaopen_act_demo \
    --output_dir=outputs/humanaopen_smolvla_demo \
    --batch_size=4 \
    --steps=20
```

> **Note** : SmolVLA (~450M params) est ~20x plus lourd que ACT (~52M), utilise plus de VRAM,
> et s'entraîne plus lentement. Batch size 4 tient dans 8GB VRAM (RTX 5060 Ti). Pour >50 épisodes,
> augmentez steps à 20000+.

### Paramètres clés

| Paramètre | Défaut | Description |
|-----------|---------|-------------|
| `--policy.type` | — | **Requis.** `act`, `smolvla`, `diffusion`, etc. |
| `--policy.device` | `cuda` | `cuda` / `cpu`. |
| `--policy.push_to_hub` | `true` | Pousser le modèle vers HuggingFace Hub. |
| `--policy.repo_id` | — | Repo Hub pour le modèle entraîné. Requis pour pousser. |
| `--dataset.repo_id` | — | **Requis.** Repo Hub du dataset d'entraînement. |
| `--output_dir` | — | Répertoire local des checkpoints. |
| `--batch_size` | 8 | Échantillons par étape. ACT : 32, SmolVLA : 4 (limite 8GB VRAM). |
| `--steps` | 100000 | Total des étapes d'entraînement. ACT : 50K, SmolVLA : 20K. |

### Sorties

```
outputs/humanaopen_act_demo/
├── pretrained_model/           # Modèle complet (config + poids)
├── last/pretrained_model       # Dernier checkpoint
├── train_logs/                 # Métriques d'entraînement (compatible TensorBoard)
└── training_state.json         # État optimiseur/scheduler pour reprise
```

Le modèle poussé sera à `https://huggingface.co/votre-nom/humanaopen_act_policy`.

## Inférence (Déploiement)

> **Dépendances** : SmolVLA nécessite `transformers>=4.48` et `num2words`.
> Installez avec `pip install transformers>=4.48 num2words` avant l'inférence SmolVLA.

### Inférence ACT 

**Double machine (recommandé)** : le robot exécute un Host (Jetson/Raspberry Pi)
avec les caméras ; `eval_data.py` s'y connecte via ZMQ sur votre PC. Démarrez le
Host d'abord, puis :

```bash
# Sur le robot (Jetson ou Raspberry Pi) — démarrez le Host et laissez-le tourner
#   (HumanaOpenHost(...).run() avec port1/port2 + les 3 caméras).

# Sur votre PC — lancez l'inférence
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=votre-nom/humanaopen_act_policy \
    --policy.device=cuda \
    --remote_ip=192.168.1.9 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --enable-base=false \
    --enable-lift=false \
    --num-episodes=5 \
    --duration=30 \
    --fps=30 \
    --display=foxglove
```

- `--remote_ip` passe en mode double machine : le follower se connecte au Host
  via ZMQ (pas de `--robot.port1/port2/port3`) ; les caméras sont sur le Host.
- `--display=foxglove` (optionnel) diffuse sur l'application Foxglove du PC
  (connectez Studio à `ws://127.0.0.1:8765`). Omettez `--display` pour une
  inférence sans visualisation.

**Machine unique** (follower directement sur ports série) :
```bash
python3 examples/eval_data.py \
    --policy.type=act \
    --policy.repo_id=votre-nom/humanaopen_act_policy \
    --policy.device=cuda \
    --robot.type=humanaopen \
    --robot.id=follower \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=None \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --enable-base=false \
    --enable-lift=false \
    --num-episodes=5 \
    --duration=30 \
    --fps=30
```

### Inférence SmolVLA (conditionnée par langage)

**Double machine (recommandé)** : identique à ACT — démarrez le Host sur le robot,
lancez sur votre PC via ZMQ :

```bash
# Sur le robot — démarrez le Host et laissez-le tourner.

# Sur votre PC
python3 examples/eval_data.py \
    --policy.type=smolvla \
    --policy.repo_id=votre-nom/humanaopen_smolvla_policy \
    --policy.device=cuda \
    --task="wave hello with both arms" \
    --remote_ip=192.168.1.9 \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --enable-base=false \
    --enable-lift=false \
    --num-episodes=2 \
    --duration=10 \
    --fps=10 \
    --display=foxglove
```

**Machine unique** (follower directement sur ports série) :
```bash
python3 examples/eval_data.py \
    --policy.type=smolvla \
    --policy.repo_id=votre-nom/humanaopen_smolvla_policy \
    --policy.device=cuda \
    --task="wave hello with both arms" \
    --robot.type=humanaopen \
    --robot.id=follower \
    --robot.port1=/dev/ttyACM0 \
    --robot.port2=/dev/ttyACM1 \
    --robot.port3=None \
    --robot.cameras='{"head": {"type": "opencv", "index_or_path": "/dev/video0", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "left_wrist": {"type": "opencv", "index_or_path": "/dev/video2", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}, "right_wrist": {"type": "opencv", "index_or_path": "/dev/video4", "width": 640, "height": 480, "fps": 30, "fourcc": "MJPG"}}' \
    --enable-base=false \
    --enable-lift=false \
    --num-episodes=2 \
    --duration=10 \
    --fps=10
```

> **Note performance SmolVLA** : L'inférence VLM prend ~1s/frame (450M params). Un épisode
> de 10s à 10fps = 100 frames ≈ 100s de temps réel. Pour un déploiement temps réel,
> utilisez ACT (~50ms/frame). SmolVLA convient mieux aux tâches conditionnées par langage.

### Affichage en direct pendant l'inférence (optionnel)

L'affichage est désactivé par défaut. Ajoutez `--display` pour diffuser le rollout en direct :

```bash
# Application Foxglove (recommandé — latence de rendu plus basse)
python3 examples/eval_data.py ... --display=foxglove
# connectez Foxglove Studio à ws://127.0.0.1:8765

# Visualiseur natif Rerun
python3 examples/eval_data.py ... --display=rerun

# Sans visualisation (défaut) : omettez --display
python3 examples/eval_data.py ...
```

> L'affichage tourne dans un thread d'arrière-plan, il ne ralentit jamais la boucle
> de politique. Comme en teleop/enregistrement, le délai de rendu de ~1–1,5s est
> inhérent au visualiseur et n'affecte pas le contrôle.

### Contrôle de la base (désactivé par défaut)

Par défaut, la base est **désactivée** (`--enable-base=false`) : les `x.vel` /
`theta.vel` prédits par la politique sont forcés à `0`, donc seuls les bras, la
tête et la levée bougent. Cela évite que le robot parte tout seul, plus sûr
pendant la validation d'une nouvelle politique.

```bash
# Base désactivée (défaut, plus sûr) — les roues restent immobiles
python3 examples/eval_data.py ... --enable-base=false

# Base activée — la politique peut piloter les roues
python3 examples/eval_data.py ... --enable-base=true
```

Commencez avec `--enable-base=false` jusqu'à ce que la politique se comporte bien,
puis activez la base si votre tâche nécessite de se déplacer.

### Contrôle de la levée (hauteur maintenue par défaut)

Par défaut, la levée est **maintenue à sa hauteur actuelle** (`--enable-lift=false`) :
le `lift_axis.height_mm` prédit par la politique est remplacé par la hauteur actuelle
à chaque image, donc la levée ne bouge pas (sinon la politique peut sortir 0 et
entraîner la levée vers le bas).

```bash
# Levée maintenue à la hauteur actuelle (défaut, plus sûr) — la levée reste en place
python3 examples/eval_data.py ... --enable-lift=false

# Levée activée — la politique contrôle la hauteur de la levée
python3 examples/eval_data.py ... --enable-lift=true
```

Commencez avec la levée maintenue, puis activez-la quand votre tâche nécessite de
changer de hauteur.

### Contrôles pendant l'inférence

| Contrôle | Touches | Notes |
|---------|------|-------|
| Quitter | `q` | Arrêter tous les épisodes |

### Sécurité : relâchement du couple à la sortie

Lorsque vous appuyez sur `q` / Ctrl+C pour arrêter l'inférence, le script :
1. **Arrête les roues de la base** (envoie `x.vel=0 / theta.vel=0` en dernier) et
   maintient la levée à sa hauteur actuelle
2. Sauvegarde la position de la levée
3. Invite : **"Press ENTER to release torque and disconnect..."**
4. Tenez les bras avant d'appuyer sur ENTER — le couple est relâché et les bras tombent librement
5. Appuyez sur ENTER quand vous êtes prêt → déconnexion

Cela évite que les bras chutent brusquement quand les servos perdent l'alimentation.

**Filet de sécurité d'arrêt automatique base/levée (double machine)** : le Host
exécute un chien de garde — si aucune commande d'action n'arrive pendant
`watchdog_timeout_ms` (500 ms), il met les roues à zéro et maintient la levée.
Ainsi, même si le processus PC est tué brutalement (`kill -9`) ou se déconnecte
pendant que la base bouge, elle s'arrête d'elle-même au lieu de continuer jusqu'à
l'arrêt du Host.

## Feuille de route

| Module | État |
|--------|------|
| URDF | ☐ |
| Préhension basée vision | ☐ |
| Navigation | ☐ |
| Collecte de données | ☐ |
| Modèles du monde incarnés | ☐ |

### Remerciements

- Le logiciel est construit sur [LeRobot](https://github.com/huggingface/lerobot)
  et [open-arms-mini](https://github.com/TheRobotStudio/open-arms-mini).
- La conception matérielle s'inspire de [xlerobot](https://github.com/xrobot/xlerobot) :
  les degrés de liberté de la tête et la base à entraînement différentiel suivent
  son approche.

## Licence

Apache 2.0
