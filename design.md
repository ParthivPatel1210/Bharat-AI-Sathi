# Bharat AI Sathi - System Design

## 1. System Overview

Bharat AI Sathi is a web-based application built using Flask.
It follows a structured MVC-like architecture.

User → Flask Server → JSON Data → Rendered Templates

## 2. Architecture

Frontend:
- HTML
- Bootstrap
- Jinja Templates

Backend:
- Flask Application
- Routes for categories and schemes
- JSON-based data management

Data Layer:
- schemes.json
- Organized by category keys
- Each category contains scheme objects

## 3. Data Structure

{
  "category_key": {
    "name": "Category Name",
    "schemes": {
      "scheme_id": {
        "title": "",
        "objective": "",
        "benefits": [],
        "eligibility": "",
        "apply": "",
        "documents": "",
        "helpline": ""
      }
    }
  }
}

## 4. Core Components

1. Home Page
   - Displays all scheme categories.

2. Category Page
   - Lists schemes under selected category.

3. Scheme Details Page
   - Displays full scheme information.

## 5. Flow Diagram

User selects category
↓
Flask route loads category from JSON
↓
User selects scheme
↓
Flask renders scheme detail page

## 6. Scalability

- Can migrate JSON to database (PostgreSQL/MySQL)
- Can integrate OpenAI API for smart Q&A
- Can implement REST API for mobile app integration

## 7. Security Considerations

- Input validation
- Secure deployment (HTTPS)
- Environment variable management for API keys

