# PDFPreview Component Technical Documentation

## Overview
The `PDFPreview` component is a React component designed to display PDF documents in different states of the generation process. It provides visual feedback to users while a PDF is being generated and offers a clean preview once the document is ready.

## Component Props
The component accepts two props:

| Prop        | Type    | Description                                                  |
| ----------- | ------- | ------------------------------------------------------------ |
| `pdfUrl`    | String  | URL pointing to the PDF document to be displayed             |
| `isLoading` | Boolean | Flag indicating whether the PDF is currently being generated |

## States
The component has three distinct states:

1. **Loading State**: When `isLoading` is `true`, displays a loading spinner
2. **Empty State**: When `pdfUrl` is not provided and `isLoading` is `false`
3. **Preview State**: When `pdfUrl` is provided and `isLoading` is `false`

## Code Structure
The component uses conditional rendering to switch between the three states based on prop values.

## Styling
The component uses Tailwind CSS classes for styling:
- Consistent height (`min-h-[800px]`) across all states
- Rounded borders with border styling that changes based on the state
- Loading state includes an animated spinner and informative text
- Empty state displays a dashed border with a prompt
- Preview state embeds the PDF in an iframe with subtle shadow styling

## Usage Example
```jsx
import PDFPreview from './PDFPreview';

// In your component:
const MyComponent = () => {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  
  const generatePDF = async () => {
    setIsGenerating(true);
    // PDF generation logic here
    const url = await yourPDFGenerationFunction();
    setPdfUrl(url);
    setIsGenerating(false);
  };

  return (
    <div>
      <button onClick={generatePDF}>Generate PDF</button>
      <PDFPreview pdfUrl={pdfUrl} isLoading={isGenerating} />
    </div>
  );
};
```

## Accessibility Considerations
- The iframe includes a title attribute for screen readers
- Loading state communicates status with both visual (spinner) and text cues

## Browser Compatibility
- Uses standard iframe for PDF display which works in most modern browsers
- No specific polyfills required

## Performance Notes
- Minimal re-renders due to simple prop-based conditional rendering
- The iframe only loads the PDF when a valid URL is provided