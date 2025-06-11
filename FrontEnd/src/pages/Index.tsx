
import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowRight, Upload, Search, UserCheck, PieChart, CheckCircle, BriefcaseBusiness } from "lucide-react";
import Navbar from "@/components/Navbar";
import FeatureCard from "@/components/FeatureCard";
import TestimonialCard from "@/components/TestimonialCard";

const Index = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      {/* Hero Section */}
      <section className="hero-gradient pt-16 pb-24 md:pt-24 md:pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row items-center">
            <div className="lg:w-1/2 lg:pr-12 mb-10 lg:mb-0">
              <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white animate-fade-up" style={{ animationDelay: "0.1s" }}>
                Your Smart Job-Hunting 
                <span className="text-blue-600 dark:text-blue-400 block mt-2">
                  Assistant
                </span>
              </h1>
              <p className="mt-6 text-xl text-gray-600 dark:text-gray-300 animate-fade-up" style={{ animationDelay: "0.3s" }}>
                Upload your resume, and let our AI assistant automatically find and apply to the perfect jobs for you. Save time and increase your chances of landing your dream job.
              </p>
              <div className="mt-8 flex flex-wrap gap-4 animate-fade-up" style={{ animationDelay: "0.5s" }}>
                <Link to="/signup">
                  <Button className="btn-gradient text-lg px-8 py-6">
                    Get Started
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Link to="/about">
                  <Button variant="outline" className="text-lg px-8 py-6">
                    Learn More
                  </Button>
                </Link>
              </div>
            </div>
            <div className="lg:w-1/2 animate-fade-in" style={{ animationDelay: "0.7s" }}>
              <img
                src="https://images.unsplash.com/photo-1573497620053-ea5300f94f21?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
                alt="Job seeker with laptop"
                className="rounded-xl shadow-xl w-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 md:py-24 bg-gray-50 dark:bg-slate-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">
              How JobBoost Works
            </h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Our AI-powered platform streamlines your job search, automating the tedious parts so you can focus on preparing for interviews.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Upload size={24} />}
              title="Upload Your Resume"
              description="Upload your resume once and our AI will extract your skills, experience, and preferences."
            />
            <FeatureCard
              icon={<Search size={24} />}
              title="Smart Job Matching"
              description="Our algorithm finds jobs that match your profile with high accuracy and relevance scores."
            />
            <FeatureCard
              icon={<UserCheck size={24} />}
              title="Automated Applications"
              description="Set your preferences and let our system automatically apply to matched jobs on your behalf."
            />
            <FeatureCard
              icon={<PieChart size={24} />}
              title="Insights Dashboard"
              description="Track your application stats and gain insights on how to improve your job search strategy."
            />
            <FeatureCard
              icon={<CheckCircle size={24} />}
              title="Interview Preparation"
              description="Get custom interview prep materials tailored to each job you're applying for."
            />
            <FeatureCard
              icon={<BriefcaseBusiness size={24} />}
              title="Career Growth"
              description="Access resources to help you grow professionally and track your career progress."
            />
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 md:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white">
              Success Stories
            </h2>
            <p className="mt-4 text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              See how JobBoost has helped job seekers land their dream roles.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <TestimonialCard
              content="I was spending hours each day applying for jobs. With JobBoost, I applied to over 50 relevant positions in just a week and landed 5 interviews!"
              author="Alex Johnson"
              role="Software Engineer"
              avatarUrl="https://randomuser.me/api/portraits/men/32.jpg"
            />
            <TestimonialCard
              content="The automated job matching saved my time and mental energy during my job search. I landed a position that pays 30% more than my previous role."
              author="Sarah Williams"
              role="Marketing Manager"
              avatarUrl="https://randomuser.me/api/portraits/women/44.jpg"
            />
            <TestimonialCard
              content="As a recent graduate, I was overwhelmed by the job market. JobBoost helped me find entry-level positions that actually matched my skills and interests."
              author="Kevin Zhang"
              role="Data Analyst"
              avatarUrl="https://randomuser.me/api/portraits/men/36.jpg"
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 md:py-24 bg-blue-600 dark:bg-blue-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold">
            Ready to Supercharge Your Job Search?
          </h2>
          <p className="mt-4 text-xl max-w-3xl mx-auto text-white/90">
            Join thousands of job seekers who have streamlined their job hunt process and found their dream jobs faster.
          </p>
          <div className="mt-10">
            <Link to="/signup">
              <Button className="bg-white text-blue-600 hover:bg-gray-100 text-lg px-8 py-6">
                Get Started for Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-100 dark:bg-slate-900 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-8 md:mb-0">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                JobBoost
              </div>
              <p className="mt-2 text-gray-600 dark:text-gray-300">
                Your smart job-hunting assistant
              </p>
            </div>
            <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-8">
              <div className="text-center md:text-left">
                <h3 className="font-medium text-gray-900 dark:text-white">Quick Links</h3>
                <ul className="mt-2 space-y-2">
                  <li>
                    <Link to="/about" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
                      About
                    </Link>
                  </li>
                  <li>
                    <Link to="/features" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
                      Features
                    </Link>
                  </li>
                  <li>
                    <Link to="/pricing" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
                      Pricing
                    </Link>
                  </li>
                </ul>
              </div>
              <div className="text-center md:text-left">
                <h3 className="font-medium text-gray-900 dark:text-white">Support</h3>
                <ul className="mt-2 space-y-2">
                  <li>
                    <Link to="/faq" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
                      FAQ
                    </Link>
                  </li>
                  <li>
                    <Link to="/contact" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
                      Contact
                    </Link>
                  </li>
                  <li>
                    <Link to="/privacy" className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">
                      Privacy
                    </Link>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-800 text-center">
            <p className="text-gray-600 dark:text-gray-300">
              &copy; {new Date().getFullYear()} JobBoost. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
