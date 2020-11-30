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
      menuItem("Keywords Analysis", tabName = "title", icon = icon("key"))
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
            p(style="text-align:justify", "From the Sunburst chart, we have the top 5 hottest selling products in the 2nd half of 2019: Men Shoes, Motor, Women's Shoes and Clothing, Sport and Outdoor & Mother and Baby. These 5 product categories make up to ", strong("40% of the total sales quantity.")),
            p(style="text-align:justify", 'These figures reflect a general trend of top-selling items in online shopping. Hence, if someone wants to become the highest "niubility" online seller on the platform, ', strong("they should focus on the Mother & Baby products,"), "which is the top sales product overall (~10% of total sales quantity). In the next analysis, our team presumed the online seller has decided to sell Mother & Baby products."),
            p(style="text-align:justify", "You can click into the sunburst chart to see more information!")
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
            div(
              p(style="text-align:justify", "Pricing is crucial in online selling, lower prices might attract customers, but may cause a backfire on profit. To find the optimum discount rate, a regression model was used to predict the actual price (less discount) from original price of Mother & Baby products."),
              p(style="text-align:justify", "The optimum discount rate is 47.67% and the actual price is predicted by the regression formula:"),
              p(style="font-style:italic", HTML("Predicted Actual Price <br>= 0.52 Original Price + 0.86")),
              inputPanel(
                textInput(
                  inputId = "price_ori",
                  label = "Original Price: ",
                  placeholder = "RM 0.00"
                ),
                span(
                  actionButton('submit', 'GO!', width="100%"),
                  style = "float:right"
                )
              ),
              inputPanel(
                p(strong("Actual Price: ")),
                textOutput("predict")
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
                HTML("Which Keywords are Important?")
              )
            ),
            "", width = 12, color = "blue"
          )
        ),
        sidebarLayout(
          sidebarPanel(
            width = 3,
            p(style="text-align:justify", "With the help of Natural Language Processing (NLP) in analyzing the product title, the output was presented in Word Cloud. The bigger the word showed, the more important the keyword is."),
            p(style="text-align:justify", "By using the TF-IDF model, we found out the following words are fairly important in the product title:", strong("Animal, Freezer, Home, Prado & Picnic."), "It is recommended to include these words in the product title, to catch customers' eyeballs."),
            p(style="text-align:justify", "We also observed that the appearance of proper nouns in the bags of keywords: Prado, XJING, Aldo, Prefeclan, Groboc, etc. Hence, it is also advised to ", strong("have a specific brand name in the product title.")),
            p("Thanks for Watching!"),
            a(href="https://github.com/Rexpert/datathon2020", target="_blank", "Bring me to Source Code!")
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
      "title" = "Keywords Analysis")
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

