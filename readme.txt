CHAIN-OF-CUSTODY
A React-based web application to manage and track the chain of custody for assets or documents. It provideTech Stack
- Frontend: ReactJS
- Styling: Tailwind CSS
- Routing: React Router DOM
- Icons: Lucide React
- Development Server: Vite

Folder Structure
CHAIN-OF-CUSTODY/
public/ # Static files like favicon, images
src/
components/ # Reusable UI components
pages/ # Page-specific components
App.jsx # App routes and layout
main.jsx # Entry point for React
.gitignore
index.html
package.json
tailwind.config.js
vite.config.js

Getting Started
Prerequisites
- Node.js (v16 or later recommended)
- npm or yarn installed
1. Clone the Repository
git clone https://github.com/lokeshparasuraman/CHAIN-OF-CUSTODY.git
cd CHAIN-OF-CUSTODY
2. Install Dependencies
npm install
# or
yarn install
3. Run the App Locally
npm run dev
# or
yarn dev
Visit: http://localhost:5173
4. Build for Production
npm run build
# or
yarn build
5. Preview Production Build
npm run preview
# or

yarn preview
Usage Guide
- Navigate between pages using the app menu.
- Add/Edit custody records using the respective forms.
- Use Lucide icons to improve accessibility and usability.
Customization
- Tailwind configuration: tailwind.config.js
- Routing logic: src/App.jsx
- Main components: src/components/
- Add new pages in: src/pages/
Contribution
Contributions are welcome! Here’s how:
1. Fork the repo
2. Create a branch (git checkout -b feature-name)
3. Commit your changes (git commit -m 'Add feature')
4. Push to the branch (git push origin feature-name)
5. Open a pull request

License
This project is licensed under the MIT License.

Author
Lokesh Parasuraman
- GitHub:https://github.com/lokeshparasuraman
- Email: lokeshparasu@gmail.com
