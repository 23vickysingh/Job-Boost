
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Upload, FileText, Check, AlertCircle } from "lucide-react";
import Navbar from '@/components/Navbar';

const ResumeUpload = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadComplete, setUploadComplete] = useState(false);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      validateAndSetFile(droppedFile);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file: File) => {
    // Check file type (PDF, DOCX, etc.)
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (!validTypes.includes(file.type)) {
      toast.error("Please upload a PDF or DOCX file");
      return;
    }
    
    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error("File size should be less than 5MB");
      return;
    }
    
    setFile(file);
    toast.success(`File "${file.name}" selected`);
  };

  const handleUpload = () => {
    if (!file) return;
    
    setIsUploading(true);
    setUploadProgress(0);
    
    // Simulating upload progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          setUploadComplete(true);
          toast.success("Resume uploaded successfully!");
          setTimeout(() => {
            navigate('/dashboard');
          }, 2000);
          return 100;
        }
        return prev + 10;
      });
    }, 300);
  };

  const resetUpload = () => {
    setFile(null);
    setUploadProgress(0);
    setUploadComplete(false);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-1 hero-gradient py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto animate-fade-up">
          <div className="text-center mb-10">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Upload Your Resume</h1>
            <p className="mt-3 text-lg text-gray-600 dark:text-gray-300">
              Let our AI analyze your resume and find the perfect job matches for you
            </p>
          </div>

          <Card className="p-6 shadow-lg glass-card">
            {!uploadComplete ? (
              <>
                <div
                  className={`border-2 border-dashed rounded-lg p-10 text-center transition-colors ${
                    isDragging
                      ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
                      : "border-gray-300 dark:border-gray-700"
                  }`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <div className="mx-auto flex justify-center mb-4">
                    <Upload
                      className={`h-12 w-12 ${
                        isDragging
                          ? "text-blue-500"
                          : "text-gray-400 dark:text-gray-500"
                      }`}
                    />
                  </div>
                  <p className="text-lg font-medium mb-2">
                    {isDragging ? "Drop your file here" : "Drag and drop your resume here"}
                  </p>
                  <p className="text-gray-500 dark:text-gray-400 mb-4">
                    or browse from your computer
                  </p>
                  <Button
                    variant="outline"
                    onClick={() => document.getElementById("resumeInput")?.click()}
                    disabled={isUploading}
                  >
                    Browse Files
                  </Button>
                  <input
                    id="resumeInput"
                    type="file"
                    className="hidden"
                    accept=".pdf,.doc,.docx"
                    onChange={handleFileChange}
                    disabled={isUploading}
                  />
                </div>

                {file && (
                  <div className="mt-6">
                    <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 flex items-start">
                      <div className="flex-shrink-0 p-2 bg-blue-100 dark:bg-blue-900/30 rounded-full mr-4">
                        <FileText className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-gray-900 dark:text-white truncate">
                          {file.name}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-red-600 hover:text-red-700 dark:text-red-400"
                        onClick={resetUpload}
                        disabled={isUploading}
                      >
                        Remove
                      </Button>
                    </div>

                    {isUploading && (
                      <div className="mt-4">
                        <div className="flex justify-between text-sm mb-1">
                          <span>Uploading...</span>
                          <span>{uploadProgress}%</span>
                        </div>
                        <Progress value={uploadProgress} className="h-2" />
                      </div>
                    )}

                    <div className="mt-6 flex justify-end">
                      <Button onClick={handleUpload} disabled={isUploading}>
                        {isUploading ? "Uploading..." : "Upload Resume"}
                      </Button>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="text-center py-8">
                <div className="mx-auto flex justify-center mb-4">
                  <div className="rounded-full bg-green-100 dark:bg-green-900/30 p-3">
                    <Check className="h-8 w-8 text-green-600 dark:text-green-400" />
                  </div>
                </div>
                <h3 className="text-xl font-semibold mb-2">Resume Uploaded Successfully!</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Our AI is analyzing your resume and finding the best job matches for you.
                </p>
                <div className="animate-pulse">
                  <p className="text-blue-600 dark:text-blue-400">
                    Redirecting to dashboard...
                  </p>
                </div>
              </div>
            )}
          </Card>

          <div className="mt-8">
            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-100 dark:border-blue-800">
              <div className="flex">
                <div className="flex-shrink-0">
                  <AlertCircle className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-blue-800 dark:text-blue-300">
                    Supported File Formats
                  </h3>
                  <div className="mt-2 text-sm text-blue-700 dark:text-blue-400">
                    <p>
                      We support PDF and DOCX formats. For best results, make sure your resume:
                    </p>
                    <ul className="list-disc pl-5 mt-1 space-y-1">
                      <li>Is less than 5MB in size</li>
                      <li>Has clear section headings</li>
                      <li>Includes your skills, experience, and education</li>
                      <li>Is free from complex tables or graphics</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumeUpload;
