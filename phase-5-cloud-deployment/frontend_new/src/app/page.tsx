import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-teal-50 to-cyan-100">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
              <div className="sm:text-center lg:text-left">
                <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                  <span className="block xl:inline">Manage your tasks</span>{' '}
                  <span className="block text-emerald-600 xl:inline">with TaskManager Pro</span>
                </h1>
                <p className="mt-3 text-base text-gray-600 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                  TaskManager Pro is a simple and effective way to keep track of everything you need to do. Sign up today to start organizing your life with our secure and reliable task management solution.
                </p>
                <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                  <div className="rounded-md shadow">
                    <Link
                      href="/signup"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-700 md:py-4 md:text-lg md:px-10 transition duration-300 ease-in-out transform hover:-translate-y-1 shadow-lg"
                    >
                      Get started
                    </Link>
                  </div>
                  <div className="mt-3 sm:mt-0 sm:ml-3">
                    <Link
                      href="/login"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-emerald-700 bg-emerald-100 hover:bg-emerald-200 md:py-4 md:text-lg md:px-10 transition duration-300 ease-in-out transform hover:-translate-y-1"
                    >
                      Sign in
                    </Link>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </div>
        <div className="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
          <div className="h-56 w-full bg-gradient-to-br from-teal-50 to-cyan-100 sm:h-72 md:h-96 lg:w-full lg:h-full">
            <div className="flex items-center justify-center h-full">
              <div className="text-center p-8">
                <div className="inline-block bg-white/80 backdrop-blur-sm p-6 rounded-2xl shadow-xl border border-white/20">
                  <div className="text-emerald-600">
                    <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                    </svg>
                  </div>
                  <h3 className="mt-4 text-lg font-medium text-gray-900">Task Management Made Simple</h3>
                  <p className="mt-2 text-gray-600">Organize, track, and complete your tasks efficiently</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-gradient-to-b from-white to-teal-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4">
              Features
            </h2>
            <p className="mt-4 max-w-2xl text-xl text-gray-600 lg:mx-auto">
              TaskManager Pro provides all the tools you need to manage your tasks effectively and securely.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {/* Feature 1: Secure Authentication */}
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-emerald-100 text-emerald-600 mb-6">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Secure Authentication</h3>
              <p className="text-gray-600">
                Enterprise-grade security with JWT authentication and encrypted data transmission.
              </p>
            </div>

            {/* Feature 2: Smart Task Management */}
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-emerald-100 text-emerald-600 mb-6">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Smart Task Management</h3>
              <p className="text-gray-600">
                Create, organize, and prioritize your tasks with our intuitive interface.
              </p>
            </div>

            {/* Feature 3: Fast & Reliable */}
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-emerald-100 text-emerald-600 mb-6">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Fast & Reliable</h3>
              <p className="text-gray-600">
                Lightning-fast performance with 99.9% uptime guarantee for your peace of mind.
              </p>
            </div>

            {/* Feature 4: User Isolation */}
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-center h-12 w-12 rounded-full bg-emerald-100 text-emerald-600 mb-6">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">User Isolation</h3>
              <p className="text-gray-600">
                Your data remains private and secure with strict user isolation protocols.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Additional Clean Section - Value Proposition */}
      <div className="py-16 bg-gradient-to-r from-emerald-50 to-teal-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-2 lg:gap-16 items-center">
            <div>
              <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
                Why Choose TaskManager Pro?
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                We believe that productivity should be simple, secure, and beautiful. Our platform combines powerful features with an elegant design to help you achieve more with less stress.
              </p>
              <dl className="mt-10 space-y-10">
                <div className="relative">
                  <dt>
                    <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-emerald-500 text-white">
                      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                    </div>
                    <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Trusted Security</p>
                  </dt>
                  <dd className="mt-2 ml-16 text-base text-gray-600">
                    Your data is protected with industry-leading encryption and security protocols.
                  </dd>
                </div>

                <div className="relative">
                  <dt>
                    <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-emerald-500 text-white">
                      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                    <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Lightning Fast</p>
                  </dt>
                  <dd className="mt-2 ml-16 text-base text-gray-600">
                    Experience near-instantaneous responses and seamless task management.
                  </dd>
                </div>

                <div className="relative">
                  <dt>
                    <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-emerald-500 text-white">
                      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                      </svg>
                    </div>
                    <p className="ml-16 text-lg leading-6 font-medium text-gray-900">Intuitive Design</p>
                  </dt>
                  <dd className="mt-2 ml-16 text-base text-gray-600">
                    Clean, modern interface designed to reduce cognitive load and increase focus.
                  </dd>
                </div>
              </dl>
            </div>
            <div className="mt-10 lg:mt-0">
              <div className="relative">
                <div className="relative rounded-2xl shadow-xl overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-r from-emerald-400 to-cyan-500 opacity-75"></div>
                  <div className="relative bg-white bg-opacity-90 p-8 rounded-2xl">
                    <div className="aspect-w-16 aspect-h-9 rounded-xl overflow-hidden">
                      <div className="bg-gradient-to-br from-teal-100 to-cyan-200 rounded-lg p-6">
                        <div className="space-y-4">
                          <div className="flex items-center">
                            <div className="h-3 w-3 bg-emerald-500 rounded-full"></div>
                            <div className="ml-3 h-2 bg-gray-200 rounded w-3/4"></div>
                          </div>
                          <div className="flex items-center">
                            <div className="h-3 w-3 bg-orange-500 rounded-full"></div>
                            <div className="ml-3 h-2 bg-gray-200 rounded w-1/2"></div>
                          </div>
                          <div className="flex items-center">
                            <div className="h-3 w-3 bg-emerald-500 rounded-full"></div>
                            <div className="ml-3 h-2 bg-gray-200 rounded w-5/6"></div>
                          </div>
                          <div className="flex items-center">
                            <div className="h-3 w-3 bg-gray-400 rounded-full"></div>
                            <div className="ml-3 h-2 bg-gray-200 rounded w-2/3"></div>
                          </div>
                        </div>
                        <div className="mt-6 pt-4 border-t border-gray-200">
                          <div className="h-2 bg-emerald-200 rounded w-1/4"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
