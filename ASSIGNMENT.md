# Project 5: Create a Riding Pelican with MCP

**Due: Tuesday 11:59 pm**
Prerequisites: run the [course setup wizard](https://drive.google.com/drive/folders/1cSlgyCejHVopVe6CdZWdKyq1rPfPujXd) before class.
The pelican riding a bicycle is [Simon Willison's test](https://simonwillison.net/2024/Oct/25/pelicans-on-a-bicycle/) of what a model can draw from one sentence. You will use both your harness from P03, and Claude to generate an animated 3D render of a riding pelican. The agent reaches Blender over a wire that delivers a server's tools, a protocol called MCP. You will write the rules for what the agent may do, and it all happens inside a sandbox that is not your laptop (in this case, GitHub Codespace).
Your pelican's ride can be any of the following:

* Through a city block at rush hour.
* Along a beach at sunset.
* Across the surface of the moon.
* Somewhere else you propose: one setting built from a few primitives.

## Instructions

* Open your codespace in VS Code using the Wizard. Blender should be already running inside a container. Start Claude Code from the sidebar and answer its folder-trust question.
* Begin with writing a Blender gate that passes acceptable requests and rejects malicious ones. Have a conversation with Claude Code to determine what the gate should accept and reject, then have it generate code to fill in offends in hooks/gate.py. It may be a good idea to have your gate print out its decisions. 
* Let’s use the harness you built back in P03 to communicate with Blender using MCP. Ask Claude Code to read harness/MCP_SPEC.md and add what it describes to your harness.py; it writes the code. Your harness should now be connected to Blender. Try creating a simple torus! harness/trace.jsonl logs every MCP call your harness makes.
* Now test your gate through your harness: ask it for a sky image from the web. The model will reach for a download tool, or try to switch downloading on from inside a script. harness/trace.jsonl should show that call refused, with the reason your gate printed. The same gate will guard Claude Code from the next step on.
* From here Claude Code is the agent, not the code writer: it drives Blender itself, under rules you write now. Open .claude/settings.json and copy from RULES.md the four tool names the ride needs into the allow list: reading the scene, reading one object, taking a screenshot, and running a script. Copy every other name into the deny list. Claude Code also runs your gate before every call, so the script check from step 2 is already in place. One of the four tools runs any Python it is handed; which one?
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
