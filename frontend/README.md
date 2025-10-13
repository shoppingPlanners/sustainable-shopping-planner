# Sustainable Shopping Frontend

Modern Next.js 14 frontend for the Sustainable Shopping Planner.

## Features

- 🏠 **Home Page** - Overview and statistics
- 🏢 **Brands Page** - Browse sustainable brands with ratings
- 🎯 **Suggestions Page** - Personalized product recommendations
- 🔥 **Trending Page** - Popular sustainable products
- 🎨 **Beautiful UI** - Tailwind CSS with modern design
- ⚡ **Fast** - Next.js 14 with App Router
- 📱 **Responsive** - Mobile-friendly design

## Quick Start

### Prerequisites

- Node.js 18+ installed
- Backend agents running on ports 5001-5004

### Installation

```bash
cd frontend
npm install
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Pages

### Home (`/`)
- System statistics
- Feature overview
- Quick links to other pages

### Brands (`/brands`)
- List of all sustainable brands
- Sustainability ratings and grades
- Certifications and commitments
- Detailed scores breakdown

### Suggestions (`/suggestions`)
- Personalized product recommendations
- User ID input (default: `demo_user`)
- Interactive feedback (Like, View, Pass)
- Detailed recommendation reasons

### Trending (`/trending`)
- Popular sustainable products
- Adjustable minimum sustainability score
- Real-time filtering

## API Integration

The frontend connects to all 4 backend agents:

- **Agent 1** (Port 5001) - Brand data
- **Agent 2** (Port 5002) - Sustainability ratings
- **Agent 3** (Port 5003) - User behavior tracking
- **Agent 4** (Port 5004) - Recommendations

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with navigation
│   ├── page.tsx            # Home page
│   ├── globals.css         # Global styles
│   ├── brands/
│   │   └── page.tsx        # Brands listing
│   ├── suggestions/
│   │   └── page.tsx        # Personalized suggestions
│   └── trending/
│       └── page.tsx        # Trending products
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

## Customization

### Change API URLs

Edit `next.config.js` to change backend URLs:

```javascript
async rewrites() {
  return [
    {
      source: '/api/brands/:path*',
      destination: 'http://your-server:5001/:path*',
    },
    // ... other rewrites
  ]
}
```

### Styling

- Modify `app/globals.css` for global styles
- Edit `tailwind.config.js` for theme customization
- Component styles use Tailwind utility classes

## Building for Production

```bash
npm run build
npm start
```

## Environment Variables

Create `.env.local`:

```bash
NEXT_PUBLIC_BRAND_COLLECTOR_URL=http://localhost:5001
NEXT_PUBLIC_RATING_CALCULATOR_URL=http://localhost:5002
NEXT_PUBLIC_USER_BEHAVIOR_URL=http://localhost:5003
NEXT_PUBLIC_SUGGESTION_URL=http://localhost:5004
```

## Technologies

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Hooks** - State management
- **Fetch API** - HTTP requests

## Tips

1. **Test User IDs**: Use different user IDs to see how recommendations change
2. **Feedback**: Click Like/View/Pass to improve future recommendations
3. **Min Score**: Adjust trending score filter to see different products
4. **Refresh**: Data updates automatically on page load

## Troubleshooting

### Agents not connecting

Make sure all backend agents are running:

```bash
# Check agent status
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
curl http://localhost:5004/health
```

### Port already in use

Change the development port:

```bash
npm run dev -- -p 3001
```

### CORS issues

The backend agents have CORS enabled for all origins in development.

## Support

For issues or questions, check the main project documentation.

