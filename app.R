# setwd("D:/UNIVERSITY UTARA MALAYSIA/Datathon 2020 - Documents/datathon2020")

library(shiny)
library(shinydashboard)
library(dashboardthemes)

ui <- dashboardPage(
  title = "Niubility Online Seller",
  header = dashboardHeader(
    title = textOutput("title")
  ),
  sidebar = dashboardSidebar(
    sidebarMenu(
      id = "tabs",
      menuItem("Product Category", tabName = "cat", icon = icon("gifts")),
      menuItem("Price Prediction", tabName = "price", icon = icon("dollar-sign")),
      menuItem("Keywords in Title", tabName = "title", icon = icon("key"))
    )
  ),
  body=dashboardBody(
    shinyDashboardThemes("grey_light"),
    tags$head(includeScript("js/press_enter.js")),
    tabItems(
      tabItem(
        "cat",
        tags$style(".col-sm-3 {height: 68vh} .well {height: 100%}"),
        fluidRow(
          tags$style(".small-box.bg-yellow { background-color: #ec742c !important; color: #000000 !important; }"),
          valueBox(
            tagList(
              tags$h3(
                style = "font-style: italic;font-size: 50px;text-align: center;font-family: \"Computer Modern\"",
                HTML("What Should I Sell?")
              )
            ),
            "", width = 12, color = "yellow"
          )
        ),
        sidebarLayout(
          sidebarPanel(
            width = 3,
            p("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed augue arcu, dapibus sit amet dapibus sit amet, mattis vitae urna. Sed ac turpis."),
            p("Quisque consequat ligula turpis, ac posuere ligula mattis eu. Etiam neque elit, sagittis at quam sed, sagittis sollicitudin velit. Vestibulum moles."),
            tags$ul(
              tags$li(tags$span("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")),
              tags$li(tags$span("Donec congue libero sed facilisis laoreet.")),
              tags$li(tags$span("In vestibulum neque dignissim, suscipit dolor in, rutrum purus.")),
              tags$li(tags$span("Ut quis arcu iaculis, fermentum lacus quis, sodales leo.")),
              tags$li(tags$span("Nunc quis sapien molestie orci efficitur interdum ut mattis magna."))
            )
          ),
          mainPanel(
            width = 9,
            includeHTML("output/html_files/top5_other_categories.html")
          )
        )
      ),
      tabItem(
        "price",
        tags$style(".col-sm-3 {height: 68vh} .well {height: 100%}"),
        fluidRow(
          tags$style(".small-box.bg-green { background-color: #a4bb2c !important; color: #000000 !important; }"),
          valueBox(
            tagList(
              tags$h3(
                style = "font-style: italic;font-size: 50px;text-align: center;font-family: \"Computer Modern\"",
                HTML("How Much is the Actual Price?")
              )
            ),
            "", width = 12, color = "green"
          )
        ),
        sidebarLayout(
          sidebarPanel(
            width = 3,
            p("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed augue arcu, dapibus sit amet dapibus sit amet, mattis vitae urna. Sed ac turpis."),
            p("Quisque consequat ligula turpis, ac posuere ligula mattis eu. Etiam neque elit, sagittis at quam sed, sagittis sollicitudin velit. Vestibulum moles."),
            inputPanel(
              textInput(
                inputId = "price_ori",
                label = "Original Price: ",
                placeholder = "RM 0.00"
              ),
              splitLayout(
                cellWidths = c("65%", "35%"),"",
                actionButton("submit", "GO!", width = "100%")
              )
            ),
            inputPanel(
              p(strong("Actual Price: ")),
              fluidRow(
                style = "height: 10vh;",
                column(9, textOutput("predict"))
              )
            )
          ),
          mainPanel(
            width = 9,
            includeHTML("output/html_files/scatter.html")
          )
        )
      ),
      tabItem(
        "title",
        tags$style(".col-sm-3 {height: 68vh} .well {height: 100%}"),
        fluidRow(
          tags$style(".small-box.bg-blue { background-color: #042b5b !important; color: #000000 !important; }"),
          valueBox(
            tagList(
              tags$h3(
                style = "font-style: italic;font-size: 50px;text-align: center;font-family: \"Computer Modern\"",
                HTML("Which Keywords should I put in the Title?")
              )
            ),
            "", width = 12, color = "blue"
          )
        ),
        sidebarLayout(
          sidebarPanel(
            width = 3,
            p("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed augue arcu, dapibus sit amet dapibus sit amet, mattis vitae urna. Sed ac turpis."),
            p("Quisque consequat ligula turpis, ac posuere ligula mattis eu. Etiam neque elit, sagittis at quam sed, sagittis sollicitudin velit. Vestibulum moles."),
            tags$ul(
              tags$li(tags$span("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")),
              tags$li(tags$span("Donec congue libero sed facilisis laoreet.")),
              tags$li(tags$span("In vestibulum neque dignissim, suscipit dolor in, rutrum purus.")),
              tags$li(tags$span("Ut quis arcu iaculis, fermentum lacus quis, sodales leo.")),
              tags$li(tags$span("Nunc quis sapien molestie orci efficitur interdum ut mattis magna."))
            )
          ),
          mainPanel(
            width = 9,
            includeHTML("output/html_files/wordcloud.html")
          )
        )
      )
    )
  )
)

server <- function(input, output, session) {
  output$title <- renderText({
    switch (
      input$tabs,
      "cat" = "Product Category",
      "price" = "Price Prediction",
      "title" = "Keywords in Title")
  })
  val <- reactiveValues(
    predict = "RM 0.00"
  )
  observeEvent(input$submit, {
    prediction <- function(value) {
      value = as.numeric(value)
      if(!is.na(value)) {
        value = 0.858328 + value * 0.523259
        value = round(value, 2)
      } else {
        value = 0
      }
      return(paste("RM", format(value, nsmall = 2, big.mark=",")))
    }
    val$predict = prediction(input$price_ori) 
  })
  output$predict <- renderText({val$predict})
}

shinyApp(ui, server)

