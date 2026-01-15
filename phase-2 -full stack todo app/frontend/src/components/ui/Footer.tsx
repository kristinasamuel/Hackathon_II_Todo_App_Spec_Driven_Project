const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-50 border-t border-gray-200">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div className="md:flex md:items-center md:justify-between">
          <div className="flex justify-center md:justify-start">
            <p className="text-sm text-gray-600">
              &copy; {currentYear} TodoApp. All rights reserved.
            </p>
          </div>
          <div className="mt-4 md:mt-0 flex justify-center space-x-6 md:order-2">
            <a href="#" className="text-sm text-gray-500 hover:text-gray-700">
              Privacy Policy
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-gray-700">
              Terms of Service
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-gray-700">
              Contact Us
            </a>
          </div>
        </div>
        <div className="mt-4 md:mt-0 text-center md:text-left">
          <p className="text-xs text-gray-500">
            Built by Kristina – Agentic AI Developer
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;