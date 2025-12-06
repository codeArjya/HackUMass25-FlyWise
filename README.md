# _**DEVPOST STORY**_

## Inspiration
Planning trips often feels like guesswork - juggling weather data, flight delays, and costs without any clear way to predict the best time to travel. We wanted to create something that makes trip planning smart, predictive, and personalized. FlyWise was initially born out of excitement for the upcoming World Cup, when flight prices to host cities are expected to surge unpredictably. Instead of guessing when to buy, FlyWise would use real-time flight data, machine learning forecasts, and Gemini-powered AI insights to tell users exactly when to book - saving both time and money while reducing the stress of travel planning.

## What it does
FlyWise combines real-time flight and weather data with Gemini’s generative intelligence to give travelers actionable insights.
Users can input destinations or flight details, and FlyWise provides:
- Forecasted flight prices using a predictive model that simulates short-term pricing trends.
- AI-driven recommendations from Google Gemini, which crafts personalized travel advice mentioning both airports and offering real-world booking tips.
- Decision factors visualization, showing which features (like days to departure, route popularity, and day of week) most influenced the model’s recommendation.
- Confidence indicators, helping users understand how certain the system is about its “Buy” or “Wait” prediction.
- A simple UI that almost anyone can use
- All hosted seamlessly on a Vultr-powered backend with Gemini handling the intelligence layer.

## How we built it
Frontend: A minimal web interface built with React for quick and responsive interaction.
Backend: A FastAPI server deployed on Vultr Cloud, with models backed by the Amadeus API to predict flight prices.
AI Integration: Google Gemini API powers the reasoning engine - generating explanations and insights into the predicted data. 
Hosting & Infrastructure: Vultr hosts both our backend and inference layer for low latency and easy deployment.

## Challenges we ran into
Connecting and authenticating the Gemini API took significant setup effort.
Deploying the backend on Vultr required manual configuration (SSH keys, DNS, and port routing).
Integrating multiple APIs (Gemini + weather + flight data) while keeping performance smooth was tricky in a short timeframe.

## Accomplishments that we're proud of
Successfully built and deployed a fully functional AI-powered flight insights app in under 36 hours.
Used Gemini API both for building the project (code generation) and running the AI logic.
Designed a clean, intuitive UI that even non-technical users can use easily.

## What we learned
How to effectively combine generative AI with real-world APIs for a tangible product.
Hands-on experience deploying production-grade services on Vultr.
Time management under pressure when integrating multiple technologies.

## What's next for FlyWise
Integrate live flight delay data from airline APIs.
Add a user account system for personalized insights.
Expand Gemini’s role to summarize and visualize travel analytics.
Migrate to a scalable Vultr or AWS setup for continuous uptime post-hackathon.
