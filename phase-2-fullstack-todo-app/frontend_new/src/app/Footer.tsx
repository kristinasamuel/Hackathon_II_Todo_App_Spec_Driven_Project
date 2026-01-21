const Footer = () => {
  return (
    <footer className="bg-gray-800 mt-auto">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-base text-gray-400">
            © {new Date().getFullYear()} TaskManager Pro. All rights reserved.
          </p>
          <p className="mt-4 text-base text-gray-300">
            Built by Kristina – Agentic AI Developer
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;