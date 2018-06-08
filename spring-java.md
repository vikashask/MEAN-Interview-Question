Spring Interview Questions 
### Q1. What is a Spring?
  Wikipedia defines the Spring framework as “an application framework and inversion of control container for the Java platform. 
  The framework’s core features can be used by any Java application, but there are extensions for building web applications on top of 
  the Java EE platform.” Spring is essentially a lightweight, integrated framework that can be used for developing enterprise applications in java.

### Q2. Name the different modules of the Spring framework.
  Some of the important Spring Framework modules are:

  Spring Context – for dependency injection.
  Spring AOP – for aspect oriented programming.
  Spring DAO – for database operations using DAO pattern
  Spring JDBC – for JDBC and DataSource support.
  Spring ORM – for ORM tools support such as Hibernate
  Spring Web Module – for creating web applications.
  Spring MVC – Model-View-Controller implementation for creating web applications, web services etc.

### Q3. List some of the important annotations in annotation-based Spring configuration.
  The important annotations are:

  @Required
  @Autowired
  @Qualifier
  @Resource
  @PostConstruct
  @PreDestroy


Q4. Explain Bean in Spring and List the different Scopes of Spring bean.
  Beans are objects that form the backbone of a Spring application. They are managed by the Spring IoC container. In other words, a bean is an object that is instantiated, assembled, and managed by a Spring IoC container.

There are five Scopes defined in Spring beans.
  Singleton: Only one instance of the bean will be created for each container. This is the default scope for the spring beans. While using this scope, make sure spring bean doesn’t have shared instance variables otherwise it might lead to data inconsistency issues because it’s not thread-safe.
  Prototype: A new instance will be created every time the bean is requested.
  Request: This is same as prototype scope, however it’s meant to be used for web applications. A new instance of the bean will be created for each HTTP request.
  Session: A new bean will be created for each HTTP session by the container.
  Global-session: This is used to create global session beans for Portlet applications.

Q5. Explain the role of DispatcherServlet and ContextLoaderListener.
  DispatcherServlet is basically the front controller in the Spring MVC application as it loads the spring bean configuration file and initializes all the beans that have been configured. If annotations are enabled, it also scans the packages to configure any bean annotated with @Component, @Controller, @Repository or @Service annotations.
  
  ContextLoaderListener, on the other hand, is the listener to start up and shut down the WebApplicationContext in Spring root. Some of its important functions includes tying up the lifecycle of Application Context to the lifecycle of the ServletContext and automating the creation of ApplicationContext.

Q6. What are the differences between constructor injection and setter injection?
  No.	Constructor Injection	Setter Injection
   1) No Partial Injection	 Partial Injection
   2) Desn’t override the setter property	 Overrides the constructor property if both are defined.
   3)	Creates new instance if any modification occurs	Doesn’t create new instance if you change the property value
   4) Better for too many properties	 Better for few properties.

Q7. What is autowiring in Spring? What are the autowiring modes?
  Autowiring enables the programmer to inject the bean automatically. We don’t need to write explicit injection logic. Let’s see the code to inject bean using dependency injection.

<bean id=“emp” class=“com.javatpoint.Employee” autowire=“byName” />  
  The autowiring modes are given below:

  No.	Mode	Description
   1)	 no	 this is the default mode, it means autowiring is not enabled.
   2)	 byName	 Injects the bean based on the property name. It uses setter method.
   3)	 byType	 Injects the bean based on the property type. It uses setter method.
   4)	 constructor	 It injects the bean using constructor
 
