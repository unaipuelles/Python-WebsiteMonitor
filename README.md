<h1 align="center">
  Website Monitor
  <br/>
  <img src=https://img.shields.io/badge/language-pyton-blue />
  <img src=https://img.shields.io/badge/version-v1.0-green />  
</h1>
<h5 align="center">Console program to monitor webs and show statistics of responses</h5>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#app-config">App config</a> •
  <a href="#dependencies">Dependencies</a> •
  <a href="#app-run">App run</a> •
  <a href="#tests">Tests</a> •
  <a href="#improving-the-app">Improving the app</a>
</p>

---

## Overview
This is a python console program which consist on monitoring web pages and the generation of some statistics about the responses of the webs. Also prompts alerts if the websites availabilities are less than 80% in the las 2 minutes and if the webs are recovered.

## Documentation
I generated pdoc documentation for the code of the program. [Here](docs/pdoc) you can find it, you only need to open that
path into a web browser to see it properly.

This is the general layout of the project:
```
project_root/
│
├── classes/ 
├── config/
├── controller/
├── docs/
├── exceptions/
├── log/
├── model/
├── view/
├── main.py
├── README
```

All the management of this program it's done by the [config/app.ini](config/app.ini) file.

### App Config
First of all you need to set the `home_dir` which is the directory where the app is stored. You can also set other directory for the `log_dir` but with the default value it will be stored in the project log directory. 

Tip for the log: You can set `log_level=10` and you will see all the background tasks that the web monitor threads make.

If we talk about the webs that you want to monitor, you have to set them in this file. There is a section in the end of the file with the name "Webs" where you can define all the webs you want to monitor. You have three parameters: name, interval and url. Here is one example if you want to monitor Google:
```
[Google]
name = Google
interval: 2
url: https://google.com
```

## Dependencies
Before you execute the program for the first time, you must download all the dependencies. Run the next command in the project_root directory:

```
.../project_root/$ pip install -r requeriments.txt
```

## App run
To run the app you only need to execute this command:
```
.../project_root/$ python main.py
```

To exit the app you can just type `exit` in the console and the program will terminate.

## Tests
I made a few tests to inspect the generated stats that the program shows. Now I'm going to explain the big test I made
monitoring of 3 webs.

### Overview of the test
I set 3 webs for the monitoring, only the third one is managed by me, so I could stop and run it to test the alerts and
the stats. 

### Configuration
```
[Google]
name = Google
interval: 2
url: https://google.com

[StackOverflow]
name = UnaiPuelles
interval: 3
url: https://stackoverflow.com

[LocalHost]
name = Localhost
interval: 5
url: http://serisportlocal/
```

### Test run
In this section I'm going to explain the main events that happened during the app runtime. You can find all the output of
the program [here](docs/test/output.log) if you want to see it more detailed.

- [Manual] 16:52:00 => Program started with all the webs up
- [Manual] ~16:56:00 => I manually stop my localhost web page
- [Program] 16:56:33 => Alert of availability: `[ALERT] Website Localhost is DOWN. Availability=77.27, Time=17/08/2021 16:56:33`
- [Manual] ~16:58:00 => I manually start again my localhost web page
- [Program] ~16:59:33 => Alert of availability: `[ALERT] Website Localhost is UP again`
- [Manual] ~16:54:35 => Program stopped


## Improving the app
The main objective that I wanted to achieve, was to have an easy app to reimplement in the future, for example, if you 
want to implement other view (a web page with charts) or a model that work with a database or Spark. As a result, I used
MVC, so you can do it much easier.

I think that I achieved the main objective, but there are few problems that could be the first things to change
before implementing other model or view.

First of all, I have to say that I didn't make a lot of validations of the app configuration. In the web configuration
you can enter the values that you want and the app will crash when the monitor starts.

In addition, there is a problem with the responses' storage. The more time passes, the more data is stored. That's not
the problem, the problem is that the unused data it's never deleted. However, this could be easy to solve with a model
that works with a database.

Finally, I hope you enjoy running and inspecting the project as I enjoyed coding.


###### Unai Puelles López