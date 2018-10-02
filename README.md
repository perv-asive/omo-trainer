## The Short Version

Omo Trainer keeps track of the fluids you drink, models your pee desperation over time, and allows or denies potty breaks. It also keeps track of your accidents to learn your personal bladder capacity.

## How to Play

To begin:

1. Be generally well hydrated.
2. Don't drink significant fluids for 45 minutes or so before starting.
3. Empty your bladder immediately before starting.
4. Open the Omo Trainer app and leave it open while you go about your business.

The rules:

1. **You may not pee unless Omo Trainer gives you permission.** If you want to pee, you must ask Omo Trainer for permission using the "May I pee?" button. If you are permitted to pee, press the "Go pee." button immediately after emptying your bladder.
2. **Whenever you drink something, enter it in Omo Trainer**; move the slider to the approximate amount of fluids then press the "Drink" button once.
3. **If you have an accident, press "I can't hold it!"** This will reset the desperation meter and teach Omo Trainer about your bladder capacity.

## Other Features
* Trainers - Personalities you can give to the program to tease or otherwise inform you of whether or not you can go.

## Technical Details (Reading this spoils the fun!)

If you'd prefer for the potty permission game to remain a mystery, don't read this! This section reveals exactly how it works, and will mean you can figure out when and how you'll be allowed to pee.

### The Dice Game
=======

### The Dice Game
Omo Trainer decides potty permission based on a simple dice game: if your dice roll higher than your current desperation rating, you are allowed to go pee. Omo Trainer uses its estimate of your current bladder contents and average bladder capacity to calculate your desperation.

The elegant thing about this game is that the higher your desperation, the lower the chance you will be allowed to pee. That means being denied permission once increases the chance that you will be denied permission again. Most of the time if you ask permission when you first need to go, you will be allowed to pee, but occasionally you will be forced to hold it to the point where an accident is a real possibility.

The idea is to play this game while going about your normal day, to make things more exciting.

You might notice that after asking permission, you can't ask again for some time. This delay is not a fixed amount of time, but rather depends on how much your desperation has increased since the last time you asked. That way, having a large bladder does not give you more chances to ask permission.

### Bladder Capacity

Whenever you press "I can't hold it!" Omo Trainer records the amount it estimates you were holding and saves it between sessions. Omo Trainer uses the average of your accident amounts as your bladder capacity.

Since the only way that Omo Trainer learns about your bladder capacity is when you have an accident, it is self-correcting for Omo Trainer to underestimate your bladder capacity. After all, then you will get permission to pee less, and will have more accidents, so Omo Trainer will learn. If Omo Trainer overestimates your capacity, however, you will get permission to pee more, and will have fewer accidents, preventing Omo Trainer from learning.  This is why Omo Trainer begins by assuming a small bladder capacity of 500 mL.

If you are dehydrated to begin with, a significant percentage of fluids will not reach your bladder, leading Omo Trainer to significantly overestimate your desperation and bladder capacity. Therefore hydrate well before playing.

### The Bladder Model

Omo Trainer uses an exponential decay model for bladder filling. This is based on observing that since the volume of bodily fluids must remain constant, the rate at which the kidneys produce urine should be proportional to the amount of excess water in the body. 

The exponential decay model has been calibrated for a half-life equivalent to a urine production rate of 750 mL/hr. This is a reasonable estimate for a hydrated adult drinking a glass of water every 15-30 minutes. It makes sense to choose this rate to be on the high side because players are likely to drink a lot and it is better to err on the side of denying pee permission.

To the scientists: please note that this model is intentionally simplistic. A more realistic mathematical model would require the app to numerically solve differential equations. The complexity would not be worth it, and it isn't really feasible anyway to expect users to enter accurate data about electrolyte balance.
