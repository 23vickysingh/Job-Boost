
import React from 'react';
import Navbar from '@/components/Navbar';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

const FAQ = () => {
  const faqs = [
    {
      question: "How do I upload my resume?",
      answer: "To upload your resume, navigate to the Resume Upload page after logging in. You can either drag and drop your file or click to browse your files. We accept PDF, DOCX, and TXT formats. After uploading, our AI will analyze your resume and extract relevant information to match you with suitable job opportunities."
    },
    {
      question: "What types of resumes are supported?",
      answer: "We support various resume formats including PDF, DOCX, and TXT files. For best results, we recommend using a clean, well-structured resume with clear sections for experience, education, and skills. ATS-friendly formats are recommended for optimal parsing accuracy."
    },
    {
      question: "Are there any constraints for resume uploads?",
      answer: "Yes, there are a few constraints: maximum file size is 5MB, we only accept PDF, DOCX, and TXT formats, and your resume should be in English. Additionally, we recommend not using images, special characters, or complex formatting that might affect our parsing algorithm."
    },
    {
      question: "How does the automated job application system work?",
      answer: "Once you've uploaded your resume and set your job preferences, our system will match you with relevant opportunities based on your skills, experience, and preferences. When a high-match job is found, the system can automatically apply on your behalf, sending your profile and customized application. You'll receive notifications for each application sent and can track their status in your dashboard."
    },
    {
      question: "What are the pricing plans?",
      answer: "We offer three main pricing plans: Free (limited job matches and manual applications), Premium ($19.99/month with unlimited job matches and up to 20 auto-applications), and Enterprise ($49.99/month with unlimited auto-applications and priority support). Please visit our Pricing page for detailed information on each plan's features."
    },
    {
      question: "What is your refund policy?",
      answer: "We offer a 7-day money-back guarantee for new Premium and Enterprise subscriptions. If you're not satisfied with our service, you can request a full refund within 7 days of your initial purchase. For refunds, please contact our support team through the Help Center with your account details and reason for the refund request."
    },
    {
      question: "How accurate is the resume parsing?",
      answer: "Our AI-powered resume parser typically achieves 85-95% accuracy in extracting information from well-formatted resumes. However, complex layouts, graphics, or non-standard formatting may reduce accuracy. You can always review and edit the extracted information in your profile to ensure everything is correct."
    },
    {
      question: "Is my data secure?",
      answer: "Yes, we take data security seriously. All uploaded resumes and personal information are encrypted in transit and at rest. We comply with GDPR and other privacy regulations. Your information is only shared with employers when you apply to their positions. For more details, please review our Privacy Policy."
    }
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <div className="flex-1 bg-gray-50 dark:bg-slate-900 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Frequently Asked Questions</h1>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              Find answers to common questions about our service
            </p>
          </div>
          
          <Accordion type="single" collapsible className="space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem key={index} value={`item-${index}`} className="bg-white dark:bg-slate-800 rounded-lg shadow-sm">
                <AccordionTrigger className="px-6 py-4 text-left text-gray-900 dark:text-white font-medium">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="px-6 pb-4 pt-0 text-gray-600 dark:text-gray-300">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
          
          <div className="mt-12 text-center">
            <p className="text-gray-600 dark:text-gray-300">
              Still have questions? 
              <a href="#" className="text-blue-600 dark:text-blue-400 font-medium hover:underline ml-1">
                Contact our support team
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FAQ;
