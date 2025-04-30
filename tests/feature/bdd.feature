
Scenario-1: Adding a task with a missing title
    Given the user leaves the title field empty and submits the form 
    When the form is submitted 
    Then no task should be added

Scenario-2: User deletes a task
    Given I hae a task in my list 
    When I click the delete button for that task
    Then the task should be removed from the task list

Scenario-3: Display overdue tasks
    Given some tasks have past due dates and are not marked as completed
    When the user selects show overdue tasks 
    Then only task that are overdue and not completed should be displayed

Scenario-4: Filtering tasks with multiple criteria
    Given tasks have different categories and priorities
    When the user selects work as the catagory and high as the priority
    Then only tasks that match both the category work and priority high should be 
    displayed

Scenario-5: Long description length
    Given the user enters a long description in the form
    When the task is added 
    Then the description shoudl be limited to a certain length 

