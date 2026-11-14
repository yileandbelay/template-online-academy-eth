import './globals.css';
import Link from 'next/link';
export const metadata = { title: 'Spike B: Online Academy', description: 'Page weight spike' };
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="site">
          <Link className="logo" href="/">Mek Academy</Link>
          <nav><Link href="/courses">Browse courses</Link><a href="/am">አማ</a></nav>
        </header>
        <main>{children}</main>
        <footer className="site">Contact · Privacy · Terms · Refunds</footer>
      </body>
    </html>
  );
}
