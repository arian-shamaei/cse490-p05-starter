# Project 5: Create a Riding Pelican with MCP

# 

**Due: Tuesday 11:59 pm**
Prerequisites: run the [course setup wizard](https://drive.google.com/drive/folders/1cSlgyCejHVopVe6CdZWdKyq1rPfPujXd) before class.
The pelican riding a bicycle is [Simon Willison's test](https://simonwillison.net/2024/Oct/25/pelicans-on-a-bicycle/) of what a model can draw from one sentence. You will use both your harness from P03, and Claude to generate an animated 3D render of a riding pelican. The agent reaches Blender over a wire that delivers a server's tools, a protocol called MCP. You will write the rules for what the agent may do, and it all happens inside a sandbox that is not your laptop (in this case, GitHub Codespace).
Your pelican's ride can be any of the following:

* Through a city block at rush hour.
* Along a beach at sunset.
* Across the surface of the moon.
* Somewhere else you propose: one setting built from a few primitives.

## Instructions

* Open your codespace in VS Code using the Wizard. Blender should be already running inside it. Start Claude Code from the sidebar and answer its folder-trust question.
* Write the gate first, before anything talks to Blender: a gate that has never refused is decoration. Ask Claude Code to fill in offends in hooks/gate.py. It sees every call before it runs and returns a reason to refuse: the download tools, and any script that reaches outside your workspace. Judge the script, not the tool name. Now, who talks to Blender?
* Your harness. Hand Claude Code harness/MCP_SPEC.md and your harness.py. Then ask your harness for a red torus on top of the cube. Read harness/trace.jsonl, not the model's summary. Did a tool run?
* Ask your harness for a sky image from the web. Did the gate say no?
* In .claude/settings.json, allow the tools the ride needs. Deny the rest. RULES.md lists them all. Which one runs any Python it is handed?
* In Claude Code, ask for the scene and the motion in fixtures/scene_brief.md. Pick one setting. Add one beat of motion that is yours. Does the pelican ride?
* Ask Claude Code to finish what the brief asks. Something in it is not yours. Read trail.jsonl. Was it refused? If nothing was, ask for the forbidden thing outright.
* Ask for the render: Workbench, frames into ride/frames/. A refused step ends an ask, so ask for the render on its own. Did the legitimate work go through?
* Run python checker.py. Fix what it names. It writes your bundle.

## Turnin

By Tuesday 11:59 pm:

* Upload the bundle to the Project 5 assignment in Canvas.
* Fill out the feedback form, and stop your codespace.

## Grading

A model will autograde your submission. It checks that each step was properly followed. Every check is pass or fail. It does not judge whether your pelican is beautiful (the vote does), code style, prompt wording, or how many tries it took.

## Reference

Out of bounds: building the scene by hand in Blender's interface; switching Claude Code to its skip-all-permissions mode; any key in anything you submit.
If Claude Code breaks, VS Code's own MCP support in the codespace reaches the same server. It covers everything but Claude Code's own gate.
