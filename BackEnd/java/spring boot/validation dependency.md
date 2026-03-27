## Validation is used to ensure the data coming into your application meets specific rules, such as:
* A field must not be blank
* An email must follow correct format
* A number must be within a range, etc.

```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>

```
### ✅ 3. Common Validation Annotations
* Annotation - Description
* @NotNull - Field must not be null
* @NotBlank - Not null and trimmed string not empty
* @Size(min, max) - Validates size of string or list
* @Email - Validates email format
* @Min / @Max - Minimum/maximum value for numbers
* @Pattern(regex = "") - Regex pattern match


### Using in DTO with @Valid
```
public class UserDTO {
    @NotBlank(message = "Name is required")
    private String name;

    @Email(message = "Invalid email format")
    private String email;

    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;

    // Getters & Setters
}

Then, in your controller:

@RestController
@RequestMapping("/users")
public class UserController {

    @PostMapping
    public ResponseEntity<String> createUser(@Valid @RequestBody UserDTO user) {
        return ResponseEntity.ok("User created successfully");
    }
}

``` 