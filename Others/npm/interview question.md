> What does the command npm adduser do?

Ans = Creates or authenticates a user for the specified registry, and saves the credentials to .npmrc

>Your organization has a legal requirement to host all code on premises, but also has an engineering requirement to use 
several public NPM modules. The NPM registry is public and remotely hosted. How can you realistically satisfy both your 
legal and engineering requirements?

Ans = Set up a locally hosted private NPM registry.

>Since users of your package will not be developing it directly, which file should be ignored in the published package?

Ans = .eslintrc

>How can you restrict who can access an NPM package?

Ans = Create a private package and grant access only to those who are authorized.

>You are authoring a new NPM package, and would like a friend to try it out before you publish it to the NPM registry. 
Which command will create a tarball that your friend can easily npm install?

Ans = npm pack

>Which of the following commands will display the current set of all applied configurations?

Ans = npm config list

>An existing NPM package exists with the exact name you want to use for your package. How can you publish your package 
using that exact name?

Ans = You can publish as a scoped package, avoiding naming collisions (i.e.: @my-own-scope/jquery).

>You have just updated a dependency (such as rxjs) to a version which optionally depends upon another package 
(In this case rxjs-compat). How could you check whether rxjs-compat is installed?

Ans = Check the contents of ./node_modules/rxjs-compat

>Given a scenario where you've been using a package (such as RxJS) and you have removed it using npm uninstall rxjs, 
you notice that it is still in your ./node_modules folder. What is a possible cause for this?

Ans = Another dependency has RxJS listed as a dependency.

>You would like to publish a new beta version of your package so that users can test some new features. 
You do not want this version of the package to become the default version when users run npm install or npm update 
unless they specify that they would like the beta version. Which command do you use to publish?

Ans = npm publish --tag beta

>If you would like to try out a release candidate of the React NPM package rather than the latest stable version, 
which command would you use (assuming that the React team has published a version with the rc distribution tag)?

Ans = npm install react@rc

>Which command removes extraneous packages from a project?

npm prune

>Which npm-generated file did package authors use for locking dependencies prior to package-lock.json in NPM version 5?

npm-shrinkwrap.json
