
# NotFound Component

## Overview
The `NotFound` component is a React functional component designed to display a visually appealing 404 error page when a user navigates to a non-existent route. It features animated elements, a responsive design, and a clean user interface with a gradient background, animated bubble, and a card with a call-to-action button.

## Purpose
This component serves as a fallback UI for invalid routes, providing users with a clear message that the requested page is unavailable and offering a link to return to the home page (`/profile`). It enhances user experience with animations and a modern aesthetic.

## Dependencies
- **React**: Utilizes the `useEffect` hook for side effects (e.g., updating the document title).
- **CSS**: Inline styles with JavaScript objects and keyframes for animations.

## Component Structure
The component consists of:
- A container with a gradient background and a floating bubble animation.
- A semi-transparent card with a frosted glass effect (using `backdropFilter`).
- Text elements (heading, subheading, and description) with fade-in animations.
- A button with a gradient background and slide-in animation.
- Keyframe animations defined in a `<style>` tag for bounce, fade-in, slide-in, and float effects.

## Key Features
- **Dynamic Document Title**: Updates the browser tab title to "404 - Page Not Found" on mount.
- **Animations**: Includes bounce (for the "404" heading), fade-in (for text), slide-in (for the button), and float (for the bubble).
- **Responsive Design**: Uses flexbox for centering content and percentage-based units (`vh`) for full-screen height.
- **Styling**: Combines inline JavaScript styles with global keyframes for reusability and performance.

## Important Functions

### `useEffect` for Document Title
The `useEffect` hook updates the document title when the component mounts and ensures no cleanup is needed by returning an empty dependency array.

```javascript
useEffect(() => {
  document.title = "404 - Page Not Found";
}, []);
```

- **Purpose**: Sets the browser tab title to indicate a 404 error.
- **Parameters**: None.
- **Dependencies**: Empty array (`[]`) ensures the effect runs only once on mount.
- **Side Effects**: Modifies the `document.title` property.

## Styles
The `styles` object defines inline CSS properties for various elements using JavaScript. Key properties include:

### Container
```javascript
container: {
  height: "100vh",
  display: "flex",
  background: "#f0f9ff",
  backgroundImage: "linear-gradient(to right, #e0f4ff, #f0f9ff, #dcf3ff)",
  justifyContent: "center",
  alignItems: "center",
  flexDirection: "column",
  position: "relative",
  overflow: "hidden",
  color: "#2c5282",
  fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
}
```
- **Purpose**: Creates a full-screen, centered layout with a gradient background.
- **Key Features**: Flexbox for alignment, `overflow: hidden` to contain the bubble, and a custom font stack.

### Card
```javascript
card: {
  backgroundColor: "rgba(255, 255, 255, 0.9)",
  border: "1px solid rgba(144, 205, 244, 0.3)",
  padding: "2rem",
  borderRadius: "16px",
  boxShadow: "0 8px 32px 0 rgba(144, 205, 244, 0.2)",
  backdropFilter: "blur(8px)",
  textAlign: "center",
  zIndex: 2,
}
```
- **Purpose**: Provides a frosted glass effect for the content card.
- **Key Features**: Semi-transparent background, blur effect, and subtle shadow for depth.

### Bubble
```javascript
bubble: {
  position: "absolute",
  top: "-100px",
  left: "-100px",
  width: "300px",
  height: "300px",
  background: "radial-gradient(circle at center, #90cdf4, transparent 70%)",
  borderRadius: "50%",
  animation: "float 6s ease-in-out infinite alternate",
  opacity: 0.4,
}
```
- **Purpose**: Adds a decorative, animated element to the background.
- **Key Features**: Radial gradient, circular shape, and floating animation.

## Animations
The `keyframes` string defines CSS animations applied to various elements:

```css
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
@keyframes slideIn {
  0% { transform: translateY(20px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
@keyframes float {
  0% { transform: translateY(0) translateX(0); }
  100% { transform: translateY(20px) translateX(20px); }
}
```
- **Purpose**: Enhances visual appeal with smooth transitions and movements.
- **Usage**: Applied to the heading (`bounce`), subheading/text (`fadeIn`), button (`slideIn`), and bubble (`float`).

## Usage
To use the `NotFound` component, import and render it in a React application, typically within a router's fallback route (e.g., using `react-router-dom`).

```javascript
import { BrowserRouter, Routes, Route } from "react-router-dom";
import NotFound from "./NotFound";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## Props
The `NotFound` component accepts no props, as it is a self-contained UI element.

## Notes
- **Browser Compatibility**: The `backdropFilter` property may not be supported in older browsers (e.g., Internet Explorer). Consider a fallback for broader compatibility.
- **Performance**: Inline styles and keyframes are efficient for a single component but may be extracted to a CSS file for larger applications.
- **Accessibility**: Ensure sufficient color contrast for text and consider adding ARIA attributes for screen readers.
- **Customization**: Modify the `styles` object or `keyframes` to adjust colors, animations, or layout as needed.

