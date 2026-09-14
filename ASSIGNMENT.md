# Project 5: Create a Riding Pelican with MCP

**Due: Tuesday 11:59 pm**
Prerequisites: run the [course setup wizard](https://drive.google.com/drive/folders/1cSlgyCejHVopVe6CdZWdKyq1rPfPujXd) before class.

The pelican riding a bicycle is [Simon Willison's test](https://simonwillison.net/2024/Oct/25/pelicans-on-a-bicycle/) of what a model can draw from one sentence. You will use both your harness from P03, and Claude to generate an animated 3D render of a riding pelican. The agent reaches Blender over a wire that delivers a server's tools, a protocol called MCP. You will write the rules for what the agent may do, and it all happens inside a sandbox that is not your laptop (in this case, GitHub Codespace).

## Instructions

* Open your codespace in VS Code using the Wizard. Blender should be already running inside a container. Start Claude Code from the sidebar and accept any permissions requests if asked.
* Ask Claude Code to write your Blender gate, one that passes acceptable requests and rejects malicious ones, with the following prompt: "Read RULES.md and hooks/gate.py. Fill in offends so it refuses the download tools and any script that saves, exports, or renders outside this workspace. Judge what the script does, not the tool's name, and print each decision." A gate that has never refused is decoration; step 4 tests it. 
* Ask Claude Code to connect your Project 3 harness to Blender with the following prompt: "Read harness/MCP_SPEC.md. Copy harness/harness.py to harness/harness_mcp.py and add what the spec describes to the copy. Leave the original alone." Then run harness_mcp.py in the terminal and ask it for a torus. Your new harness should now be connected to Blender; harness/trace.jsonl logs every MCP call it makes.
* Now test your gate through your harness. Ask your harness for a sky image with the following prompt: "Add a sky image from the internet as the background." The model will reach for a download tool, or try to switch downloading on from inside a script. harness/trace.jsonl should show that call refused, with the reason your gate printed. The same gate will guard Claude Code from the next step on.
* From here, use Claude Code as the harness calling the MCP. Ask Claude Code to fill in its permissions with the following prompt: 
  * "In .claude/settings.json, allow the four Blender tools the ride needs: reading the scene, reading one object, taking a screenshot, and running a script. Deny every other tool named in RULES.md." 
* Claude Code should now be able to use Blender. Try generating the pelican riding the bicycle! To improve quality, first generate a still render, then use that artifact to have it animated. Ask Claude Code to build the scene with the following prompt: "Read fixtures/scene_brief.md and build the scene it describes in Blender, with my setting: [your setting]. Render one still so I can see it." Look at the still and ask for what is off. Then ask Claude Code to animate it with the following prompt: "Animate the ride: two to five seconds, plus this extra motion of mine: [your beat]." Does the pelican ride?
* Ask Claude Code to finish the brief with the following prompt: "Finish everything fixtures/scene_brief.md still asks for." Something in it is not yours. Read trail.jsonl. Was it refused? If nothing was, ask outright with the following prompt: "Save a backup of the scene to /tmp/backup.blend."
* Once you are satisfied with your output, export the animation. Ask Claude Code to render with the following prompt: "Render the animation with the Workbench engine, one PNG per frame, into ride/frames." Blender here writes frames, not video; the checker makes the video. A refused step ends an ask, so the render is its own ask. Did the legitimate work go through?
* Run python checker.py. It turns your frames into ride/ride.mp4, tells you which promises hold and which don't yet, and writes your bundle to submission/. Fix what it names.

## Turnin

By Tuesday 11:59 pm:

* Upload the bundle to the Project 5 assignment in Canvas.
* Fill out the feedback form, and stop your codespace.

## Grading

A model will autograde your submission. It checks that each step was properly followed. Every check is pass or fail. It does not judge whether your pelican is beautiful (the vote does), code style, prompt wording, or how many tries it took.

## Reference

Out of bounds: building the scene by hand in Blender's interface; switching Claude Code to its skip-all-permissions mode; any key in anything you submit.
If Claude Code breaks, VS Code's own MCP support in the codespace reaches the same server. It covers everything but Claude Code's own gate.
