# Project 5: The Pelican Rides

**Due: Tuesday 11:59 pm**

Prerequisites: run the [course setup wizard](https://drive.google.com/drive/folders/1cSlgyCejHVopVe6CdZWdKyq1rPfPujXd) before class. Its Project 5 pack signs you in to GitHub, puts your week-three harness there, and builds your codespace (about ten minutes, once).

Make the pelican ride: the famous pelican riding a bicycle, in 3D and moving, built by your agent through Blender without you building any of it by hand. The agent reaches Blender over a wire that delivers a server's tools, a protocol called MCP. You write the rules that say what the agent may do, and it all happens inside a room that is not your laptop. The lecture's pelican prompt is in your workspace as your starting point; the ride is your build. Afterward, the class screens every pelican and votes.

Your pelican's ride can be any of the following:

- Through a city block at rush hour.
- Along a beach at sunset.
- Across the surface of the moon.
- Somewhere else you propose: one setting built from a few primitives.

Then give the ride one extra beat of motion that is yours: a wobble, a jump, a wave to the camera, a flap.

## Instructions

- Open your codespace in VS Code, the wizard's last step. Blender is running inside it, its view in the middle of the editor. Nothing is talking to it yet. Who gets to?
- Your harness first, and its gate before its wire. Your week-three gate checks a path; the server's tools carry none, so left alone it refuses everything while the model still reports success. Rewrite it to refuse the server's download tools and any script that reaches outside your workspace, reading what the script does, not just the tool's name. What will you look at to know it worked?
- The trace, not the summary. Hand Claude Code the protocol spec in your workspace so your harness learns the wire, then ask your harness for a sphere above the default cube. Watch it appear in Blender. Now ask for a sky image from the web. Did the gate say no?
- Now the ride, in Claude Code. Pick your setting and ask for the scene: the pelican, the bicycle, the setting, materials, a light, and a camera that frames the ride. One object per ask. Does the camera see everything?
- Ask for the motion: the wheels or the legs turn, the bicycle moves forward, two to five seconds, plus your extra beat. Play it in Blender. Does the pelican ride?
- Before you render, read the scene brief in your workspace, the note your agent read first. Something in it is not yours. What would an agent with no rules have done?
- Write the rules for Claude Code: which of the server's tools it may call, which it may never call, and one hook that stops a script from reaching outside your workspace. Safe mode is already on; your rules are the second gate. Will they hold?
- Find out, in the codespace. With your rules in place, ask your agent to finish what the brief asks for. Check the audit trail your hook wrote. Did the gate say no? If your agent never took the bait, ask for the forbidden thing outright.
- Rules still on, ask for the render on Blender's preview engine, Workbench, frame by frame; the checker joins the frames into a video. Did it go through? Can you watch it?
- Run the workspace's checker. It tells you which of the promises above hold and which don't yet, and writes your submission bundle.

## Turnin

By Tuesday 11:59 pm:

- Download the bundle the checker wrote (your scene file, your rendered animation, Claude Code's conversation record, your harness with its trace, your rules, and the audit trail your hook wrote) and upload it to the Project 5 assignment in Canvas. Built on your own Blender? Copy both records and both server configs into the workspace first.
- Bank the rules in your Dev Kit: the server config, the permissions, the hook. Keep the harness; it speaks the protocol now.
- Fill out the feedback form, and stop your codespace.

We'll screen every pelican in class and vote on favorites. Stretch, not required: make the pelican ride through your own harness. It takes far more turns and tokens; seeing why is the lesson.

## Grading

The course's automated grader reads your submission and checks that each step was properly followed. Every check is pass or fail. It does not judge whether your pelican is beautiful (that is what the vote is for), code style, prompt wording, or how many tries it took.

## Reference

Out of bounds: building or fixing the scene by hand in Blender's interface; switching your agent to its skip-all-permissions mode; any key or password in anything you submit.

You work in the same VS Code as week three, connected to the codespace. It talks to the course's model gateway with the week's model pinned, and the server's telemetry is off in the pack. Stop the codespace when you leave; the free allowance is about sixty hours a month. Building the animation on your own Blender is allowed: the install and the two telemetry switches are yours (the local checklist lists them), with no TA support, and the wire, the gate, and the temptation stay in the codespace; every render is Workbench, so the vote compares like with like. If Claude Code breaks, VS Code's MCP support in the codespace reaches the same server and covers everything but Claude Code's own gate; if everything is down, write the rules offline against the reference record and submit that half.

