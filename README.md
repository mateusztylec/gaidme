# gaidme
> Yeah, need to check if port 3000 on firewall is open.
> 
> How did it go? utf ...???? fck i don't remember. will google/chatgpt that 🥲

Do you recognize that?? Wait no more!

gaidme is an innovative command-line interface (CLI) tool designed to boost your development workflow. It utilizes AI to understand and execute system commands, making task automation, information queries, and environment management smoother and more intuitive.

## Getting Started
### Prerequisites

- Python 3.8 or higher
- Proper environment variables set. More info below or in `.env.example` file
  
#### OpenAI
```
export OPENAI_API_KEY=sk-...
```
#### AzureOpenAI
```
export AZURE_OPENAI_API_KEY=sk-...
export AZURE_OPENAI_ENDPOINT="https://docs-test-001.openai.azure.com/"
export AZURE_OPENAI_DEPLOYEMNT=gpt-4
```
#### Bash shell
```
export 'PROMPT_COMMAND=history -a';
```
### Installation

To install run:
```
pip install gaidme
``` 

## Usage
### ask

`gaidme ask {prompt}` is used to ask AI about specific action. As a result you will get command based on your request/prompt

Example:
```
$ gaidme ask find my ip addres that start with 192.168
$ ifconfig | grep 'inet 192.168' | awk '{print $2}' #this is result of the command
```
### reflect
***Note: The reflect feature is still under development and may cause unexpected behavior***

`gaidme reflect {prompt}` is used to ask AI question and as an answer you will get command based on your request/prompt. This takes previous command and output from the previous command to create tailored command based on previous command and your prompt

Steps:
- Type a command you want to reflect on, like `docker image ls`
- Use `gaidme reflect {your prompt}` to ask question about your most recent command and output from this command
- As a result you will get a tailored command based on your previous command and result of the previous command

Example:
```
$ docker image ls
REPOSITORY                  TAG       IMAGE ID       CREATED        SIZE
mateusztylec/ai-personal    latest    877c4cda4b92   7 weeks ago    1.26GB
mateusztylec/ai-assistant   latest    b770d85f07e5   7 weeks ago    1.26GB
mateusztylec/ai-personal    <none>    b770d85f07e5   7 weeks ago    1.26GB
qdrant/qdrant               latest    612cd8d1d0b7   2 months ago   175MB
postgres                    latest    ba67a00c6c50   3 months ago   447MB
$ gaidme reflect show id only
... some commands that is needed
$ docker image ls | awk '{print $3}' | uniq #this is result of the command
``` 
'reflect' command is supported only in zsh and bash

### Video (demo)

### Rules
- Do not use special characters like %#@| and other when creating the prompt

## Future development
I am currently working on my own API. It will have access to the current documentation of most popular tools. So it means more accurate responses. Do you want to get access to it? Sign up for **[waitlist](https://airtable.com/appsYU2AJudGb9B1V/pagVW8inby0MAnjP5/form)**

## Features
- Support for AzureOpenAI
- Option to edit commands before execution
- Get tailored command based on the the previous command

## Contributing and Support
We welcome contributions to gaidme! If you have suggestions for improvements or bug fixes, please feel free to submit an issue or pull request. 

If you need help or have questions, reach out to me via [GitHub Issues](https://github.com/mateusztylec/gaidme/issues).

## Buy Me A Coffee
If you find gaidme useful, consider 🥰 supporting 🥰

<a href="https://www.buymeacoffee.com/mateusztylec" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

## Keep in mind
- Tested only on zsh, sh and bash

## License
MIT