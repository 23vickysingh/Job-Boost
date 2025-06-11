
import React from 'react';
import Navbar from '@/components/Navbar';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Check } from "lucide-react";

const Pricing = () => {
  const plans = [
    {
      name: "Free",
      price: "$0",
      description: "Basic features to get started with your job search",
      features: [
        "Upload 1 resume",
        "10 job matches per month",
        "Basic profile",
        "Manual applications only",
        "Email notifications"
      ],
      popular: false,
      buttonText: "Get Started",
      buttonVariant: "outline" as const
    },
    {
      name: "Premium",
      price: "$19.99",
      period: "per month",
      description: "Advanced features for serious job seekers",
      features: [
        "Upload multiple resumes",
        "Unlimited job matches",
        "Enhanced profile customization",
        "Up to 20 auto-applications per month",
        "Priority job matching",
        "Application tracking",
        "Resume performance analytics"
      ],
      popular: true,
      buttonText: "Start Free Trial",
      buttonVariant: "default" as const
    },
    {
      name: "Enterprise",
      price: "$49.99",
      period: "per month",
      description: "Complete solution for professional job hunters",
      features: [
        "All Premium features",
        "Unlimited auto-applications",
        "Advanced analytics dashboard",
        "Personal career coach",
        "Interview preparation sessions",
        "LinkedIn profile optimization",
        "Priority support 24/7"
      ],
      popular: false,
      buttonText: "Contact Sales",
      buttonVariant: "outline" as const
    }
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <div className="flex-1 bg-gray-50 dark:bg-slate-900 py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Simple, Transparent Pricing</h1>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              Choose a plan that works best for your job search needs
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <Card key={index} className={`flex flex-col ${plan.popular ? 'ring-2 ring-blue-500 dark:ring-blue-400' : ''}`}>
                <CardHeader>
                  {plan.popular && (
                    <Badge className="w-fit mb-2 bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
                      Most Popular
                    </Badge>
                  )}
                  <CardTitle className="text-2xl font-bold">{plan.name}</CardTitle>
                  <div className="mt-2">
                    <span className="text-3xl font-bold">{plan.price}</span>
                    {plan.period && <span className="text-gray-600 dark:text-gray-300 ml-1">{plan.period}</span>}
                  </div>
                  <CardDescription className="mt-2">{plan.description}</CardDescription>
                </CardHeader>
                <CardContent className="flex-1">
                  <ul className="space-y-3">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center gap-2">
                        <Check className="h-5 w-5 text-green-500 dark:text-green-400 flex-shrink-0" />
                        <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
                <CardFooter>
                  <Button className="w-full" variant={plan.buttonVariant}>
                    {plan.buttonText}
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>
          
          <div className="mt-16 bg-white dark:bg-slate-800 rounded-lg shadow-sm p-8">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white text-center mb-8">
              Frequently Asked Questions About Pricing
            </h2>
            
            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Can I upgrade or downgrade my plan?
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Yes, you can upgrade or downgrade your plan at any time. Changes will take effect on your next billing cycle.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Do you offer a free trial?
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Yes, we offer a 7-day free trial on our Premium plan. No credit card required.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  What's your refund policy?
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  We offer a 7-day money-back guarantee on all plans. If you're not satisfied, contact support for a full refund.
                </p>
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  Do you offer discounts for annual subscriptions?
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Yes, you can save 20% by choosing annual billing on any of our paid plans.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Pricing;
