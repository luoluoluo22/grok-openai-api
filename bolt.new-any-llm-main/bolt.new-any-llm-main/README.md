[![Bolt.new: AI-Powered Full-Stack Web Development in the Browser](./public/social_preview_index.jpg)](https://bolt.new)

[English](./README.md) | [中文](./README.zh-CN.md)

# Bolt.new Fork by Cole Medin - oTToDev

This fork of Bolt.new (oTToDev) allows you to choose the LLM that you use for each prompt! Currently, you can use OpenAI, Anthropic, Ollama, OpenRouter, Gemini, LMStudio, Mistral, xAI, HuggingFace, DeepSeek, or Groq models - and it is easily extended to use any other model supported by the Vercel AI SDK! See the instructions below for running this locally and extending it to include more models.

## Join the community for oTToDev!

https://thinktank.ottomator.ai

## Requested Additions to this Fork - Feel Free to Contribute!!

- ✅ OpenRouter Integration (@coleam00)
- ✅ Gemini Integration (@jonathands)
- ✅ Autogenerate Ollama models from what is downloaded (@yunatamos)
- ✅ Filter models by provider (@jasonm23)
- ✅ Download project as ZIP (@fabwaseem)
- ✅ Improvements to the main Bolt.new prompt in `app\lib\.server\llm\prompts.ts` (@kofi-bhr)
- ✅ DeepSeek API Integration (@zenith110)
- ✅ Mistral API Integration (@ArulGandhi)
- ✅ "Open AI Like" API Integration (@ZerxZ)
- ✅ Ability to sync files (one way sync) to local folder (@muzafferkadir)
- ✅ Containerize the application with Docker for easy installation (@aaronbolton)
- ✅ Publish projects directly to GitHub (@goncaloalves)
- ✅ Ability to enter API keys in the UI (@ali00209)
- ✅ xAI Grok Beta Integration (@milutinke)
- ✅ LM Studio Integration (@karrot0)
- ✅ HuggingFace Integration (@ahsan3219)
- ✅ Bolt terminal to see the output of LLM run commands (@thecodacus)
- ✅ Streaming of code output (@thecodacus)
- ✅ Ability to revert code to earlier version (@wonderwhy-er)
- ✅ Cohere Integration (@hasanraiyan)
- ✅ Dynamic model max token length (@hasanraiyan)
- ✅ Prompt caching (@SujalXplores)
- ✅ **HIGH PRIORITY** - Load local projects into the app (@wonderwhy-er)
- ⬜ **HIGH PRIORITY** - ALMOST DONE - Attach images to prompts (@atrokhym)
- ⬜ **HIGH PRIORITY** - Prevent Bolt from rewriting files as often (file locking and diffs)
- ⬜ **HIGH PRIORITY** - Better prompting for smaller LLMs (code window sometimes doesn't start)
- ⬜ **HIGH PRIORITY** - Run agents in the backend as opposed to a single model call
- ⬜ Mobile friendly
- ⬜ Together Integration
- ⬜ Azure Open AI API Integration
- ⬜ Perplexity Integration
- ⬜ Vertex AI Integration
- ⬜ Deploy directly to Vercel/Netlify/other similar platforms
- ⬜ Better prompt enhancing
- ⬜ Have LLM plan the project in a MD file for better results/transparency
- ⬜ VSCode Integration with git-like confirmations
- ⬜ Upload documents for knowledge - UI design templates, a code base to reference coding style, etc.
- ⬜ Voice prompting

## Bolt.new: AI-Powered Full-Stack Web Development in the Browser

Bolt.new is an AI-powered web development agent that allows you to prompt, run, edit, and deploy full-stack applications directly from your browser—no local setup required. If you're here to build your own AI-powered web dev agent using the Bolt open source codebase, [click here to get started!](./CONTRIBUTING.md)

## What Makes Bolt.new Different

Claude, v0, etc are incredible- but you can't install packages, run backends, or edit code. That's where Bolt.new stands out:

- **Full-Stack in the Browser**: Bolt.new integrates cutting-edge AI models with an in-browser development environment powered by **StackBlitz's WebContainers**. This allows you to:
  - Install and run npm tools and libraries (like Vite, Next.js, and more)
  - Run Node.js servers
  - Interact with third-party APIs
  - Deploy to production from chat
  - Share your work via a URL

- **AI with Environment Control**: Unlike traditional dev environments where the AI can only assist in code generation, Bolt.new gives AI models **complete control** over the entire  environment including the filesystem, node server, package manager, terminal, and browser console. This empowers AI agents to handle the whole app lifecycle—from creation to deployment.

Whether you're an experienced developer, a PM, or a designer, Bolt.new allows you to easily build production-grade full-stack applications.

For developers interested in building their own AI-powered development tools with WebContainers, check out the open-source Bolt codebase in this repo!

## Setup

Many of you are new users to installing software from Github. If you have any installation troubles reach out and submit an "issue" using the links above, or feel free to enhance this documentation by forking, editing the instructions, and doing a pull request.

1. Install Git from https://git-scm.com/downloads

2. Install Node.js from https://nodejs.org/en/download/ 

Pay attention to the installer notes after completion. 

On all operating systems, the path to Node.js should automatically be added to your system path. But you can check your path if you want to be sure. On Windows, you can search for "edit the system environment variables" in your system, select "Environment Variables..." once you are in the system properties, and then check for a path to Node in your "Path" system variable. On a Mac or Linux machine, it will tell you to check if /usr/local/bin is in your $PATH. To determine if usr/local/bin is included in $PATH open your Terminal and run:

```
echo $PATH .
```

If you see usr/local/bin in the output then you're good to go.

3. Clone the repository (if you haven't already) by opening a Terminal window (or CMD with admin permissions) and then typing in this:

```
git clone https://github.com/coleam00/bolt.new-any-llm.git
```

3. Rename .env.example to .env.local and add your LLM API keys. You will find this file on a Mac at "[your name]/bold.new-any-llm/.env.example". For Windows and Linux the path will be similar.

![image](https://github.com/user-attachments/assets/7e6a532c-2268-401f-8310-e8d20c731328)

If you can't see the file indicated above, its likely you can't view hidden files. On Mac, open a Terminal window and enter this command below. On Windows, you will see the hidden files option in File Explorer Settings. A quick Google search will help you if you are stuck here.

```
defaults write com.apple.finder AppleShowAllFiles YES
```

**NOTE**: you only have to set the ones you want to use and Ollama doesn't need an API key because it runs locally on your computer:

Get your GROQ API Key here: https://console.groq.com/keys

Get your Open AI API Key by following these instructions: https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key

Get your Anthropic API Key in your account settings: https://console.anthropic.com/settings/keys

```
GROQ_API_KEY=XXX
OPENAI_API_KEY=XXX
ANTHROPIC_API_KEY=XXX
```

Optionally, you can set the debug level:

```
VITE_LOG_LEVEL=debug
```

And if using Ollama set the DEFAULT_NUM_CTX, the example below uses 8K context and ollama running on localhost port 11434:

```
OLLAMA_API_BASE_URL=http://localhost:11434
DEFAULT_NUM_CTX=8192
```

**Important**: Never commit your `.env.local` file to version control. It's already included in .gitignore.

## Run with Docker

Prerequisites:

Git and Node.js as mentioned above, as well as Docker: https://www.docker.com/

### 1a. Using Helper Scripts

NPM scripts are provided for convenient building:

```bash
# Development build
npm run dockerbuild

# Production build
npm run dockerbuild:prod
```

### 1b. Direct Docker Build Commands (alternative to using NPM scripts)

You can use Docker's target feature to specify the build environment instead of using NPM scripts if you wish:

```bash
# Development build
docker build . --target bolt-ai-development

# Production build
docker build . --target bolt-ai-production
```

### 2. Docker Compose with Profiles to Run the Container

Use Docker Compose profiles to manage different environments:

```bash
# Development environment
docker-compose --profile development up

# Production environment
docker-compose --profile production up
```

When you run the Docker Compose command with the development profile, any changes you
make on your machine to the code will automatically be reflected in the site running
on the container (i.e. hot reloading still applies!).

## Run Without Docker

1. Install dependencies using Terminal (or CMD in Windows with admin permissions):

```
pnpm install
```

If you get an error saying "command not found: pnpm" or similar, then that means pnpm isn't installed. You can install it via this:

```
sudo npm install -g pnpm
```

2. Start the application with the command:

```bash
pnpm run dev
```

## Adding New LLMs:

To make new LLMs available to use in this version of Bolt.new, head on over to `app/utils/constants.ts` and find the constant MODEL_LIST. Each element in this array is an object that has the model ID for the name (get this from the provider's API documentation), a label for the frontend model dropdown, and the provider. 

By default, Anthropic, OpenAI, Groq, and Ollama are implemented as providers, but the YouTube video for this repo covers how to extend this to work with more providers if you wish!

When you add a new model to the MODEL_LIST array, it will immediately be available to use when you run the app locally or reload it. For Ollama models, make sure you have the model installed already before trying to use it here!

## Available Scripts

- `pnpm run dev`: Starts the development server.
- `pnpm run build`: Builds the project.
- `pnpm run start`: Runs the built application locally using Wrangler Pages. This script uses `bindings.sh` to set up necessary bindings so you don't have to duplicate environment variables.
- `pnpm run preview`: Builds the project and then starts it locally, useful for testing the production build. Note, HTTP streaming currently doesn't work as expected with `wrangler pages dev`.
- `pnpm test`: Runs the test suite using Vitest.
- `pnpm run typecheck`: Runs TypeScript type checking.
- `pnpm run typegen`: Generates TypeScript types using Wrangler.
- `pnpm run deploy`: Builds the project and deploys it to Cloudflare Pages.

## Development

To start the development server:

```bash
pnpm run dev
```

This will start the Remix Vite development server. You will need Google Chrome Canary to run this locally if you use Chrome! It's an easy install and a good browser for web development anyway.

## FAQ

### How do I get the best results with oTToDev?

- **Be specific about your stack**: If you want to use specific frameworks or libraries (like Astro, Tailwind, ShadCN, or any other popular JavaScript framework), mention them in your initial prompt to ensure Bolt scaffolds the project accordingly.

- **Use the enhance prompt icon**: Before sending your prompt, try clicking the 'enhance' icon to have the AI model help you refine your prompt, then edit the results before submitting.

- **Scaffold the basics first, then add features**: Make sure the basic structure of your application is in place before diving into more advanced functionality. This helps oTToDev understand the foundation of your project and ensure everything is wired up right before building out more advanced functionality.

- **Batch simple instructions**: Save time by combining simple instructions into one message. For example, you can ask oTToDev to change the color scheme, add mobile responsiveness, and restart the dev server, all in one go saving you time and reducing API credit consumption significantly.

### How do I contribute to oTToDev?

[Please check out our dedicated page for contributing to oTToDev here!](CONTRIBUTING.md)

### Do you plan on merging oTToDev back into the official Bolt.new repo?

More news coming on this coming early next month - stay tuned!

### What are the future plans for oTToDev?

[Check out our Roadmap here!](https://roadmap.sh/r/ottodev-roadmap-2ovzo)

Lot more updates to this roadmap coming soon!

### Why are there so many open issues/pull requests?

oTToDev was started simply to showcase how to edit an open source project and to do something cool with local LLMs on my (@ColeMedin) YouTube channel! However, it quickly
grew into a massive community project that I am working hard to keep up with the demand of by forming a team of maintainers and getting as many people involved as I can.
That effort is going well and all of our maintainers are ABSOLUTE rockstars, but it still takes time to organize everything so we can efficiently get through all
the issues and PRs. But rest assured, we are working hard and even working on some partnerships behind the scenes to really help this project take off!

### How do local LLMs fair compared to larger models like Claude 3.5 Sonnet for oTToDev/Bolt.new?

As much as the gap is quickly closing between open source and massive close source models, you're still going to get the best results with the very large models like GPT-4o, Claude 3.5 Sonnet, and DeepSeek Coder V2 236b. This is one of the big tasks we have at hand - figuring out how to prompt better, use agents, and improve the platform as a whole to make it work better for even the smaller local LLMs!

### I'm getting the error: "There was an error processing this request"

If you see this error within oTToDev, that is just the application telling you there is a problem at a high level, and this could mean a number of different things. To find the actual error, please check BOTH the terminal where you started the application (with Docker or pnpm) and the developer console in the browser. For most browsers, you can access the developer console by pressing F12 or right clicking anywhere in the browser and selecting "Inspect". Then go to the "console" tab in the top right.

### I'm getting the error: "x-api-key header missing"

We have seen this error a couple times and for some reason just restarting the Docker container has fixed it. This seems to be Ollama specific. Another thing to try is try to run oTToDev with Docker or pnpm, whichever you didn't run first. We are still on the hunt for why this happens once and a while!

### I'm getting a blank preview when oTToDev runs my app!

We promise you that we are constantly testing new PRs coming into oTToDev and the preview is core functionality, so the application is not broken! When you get a blank preview or don't get a preview, this is generally because the LLM hallucinated bad code or incorrect commands. We are working on making this more transparent so it is obvious. Sometimes the error will appear in developer console too so check that as well.

### Everything works but the results are bad

This goes to the point above about how local LLMs are getting very powerful but you still are going to see better (sometimes much better) results with the largest LLMs like GPT-4o, Claude 3.5 Sonnet, and DeepSeek Coder V2 236b. If you are using smaller LLMs like Qwen-2.5-Coder, consider it more experimental and educational at this point. It can build smaller applications really well, which is super impressive for a local LLM, but for larger scale applications you want to use the larger LLMs still!
