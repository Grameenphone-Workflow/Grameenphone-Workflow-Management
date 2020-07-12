# Grameenphone-Workflow-Management

Visit: https://wfm.grameenphone.com/

Need to recreate the following folders:
- data/
- data/product
- data/visit_images
- data/visiting_excels

Need to recreate the following files:
- .mailserver E-mail server.
- .me -> E-mail sender address.
- .password -> E-mail sender password.
- .receivers -> E-mail reciever.
- .secret -> The Django Secret.

## Setting up automatic emails:

- Install the redis dependencies to get a server for job queueing and asynchronous execution.

```bash
$ sudo apt install redis
$ pip3 install redis
```

- Install celery to handle queueing and workers.
```bash
$ pip3 install celery
```

- Run each of these as a separate background process.
```bash
$ redis-server
$ celery -A GPWorkflow beat -l info # Must execute in GPWorkflow Project Directory.
$ celery -A GPWorkflow beat -l info # Must execute in GPWorkflow Project Directory.
```

## Related Projects:

<img width="150" src="./statics/images/workflow-lite.png"/>

Parent Project:
- [Workflow](https://github.com/Saqibur/Workflow)



Sub Projects:
1. [Visit-Tracker-Flutter-App](https://github.com/Saqibur/Visit-Tracker-Flutter-App)

<img width="150" src="./statics/images/visit-app.png"/>

2. [Visit-Tracker-API](https://github.com/Saqibur/Visit-Tracker)

<img width="150" src="./statics/images/visit-web.png"/>