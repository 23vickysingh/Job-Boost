
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Upload, FileText, Check, AlertCircle } from "lucide-react";
import Navbar from '@/components/Navbar';
import ConfirmationDialog from '@/components/ui/confirmation-dialog';
import { uploadResume } from "@/lib/api";

const ResumeUpload = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [isValidFile, setIsValidFile] = useState(false);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);
  
  // Confirmation dialog state
  const [confirmationDialog, setConfirmationDialog] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    type: 'info' | 'warning' | 'danger';
    confirmText: string;
    onConfirm: () => void;
  }>({
    isOpen: false,
    title: '',
    message: '',
    type: 'info',
    confirmText: 'Confirm',
    onConfirm: () => {}
  });

  const handleSkip = () => {
    setConfirmationDialog({
      isOpen: true,
      title: 'Skip Resume Upload',
      message: 'Are you sure you want to skip resume upload? You can upload your resume later from the dashboard.',
      type: 'warning',
      confirmText: 'Skip',
      onConfirm: () => {
        navigate('/dashboard');
      }
    });
  };

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
    const errors: string[] = [];
    
    // Check file type (PDF, DOCX only)
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const validExtensions = ['.pdf', '.docx'];
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    
    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
      errors.push("Please upload a PDF or DOCX file only");
    }
    
    // Check file size (max 1MB)
    const maxSize = 1 * 1024 * 1024; // 1MB in bytes
    if (file.size > maxSize) {
      errors.push(`File size (${(file.size / 1024 / 1024).toFixed(2)} MB) exceeds maximum allowed size of 1 MB`);
    }
    
    if (errors.length > 0) {
      setValidationErrors(errors);
      setIsValidFile(false);
      setFile(file); // Still set the file to show it, but mark as invalid
      
      // Show validation error dialog
      setConfirmationDialog({
        isOpen: true,
        title: 'Invalid File',
        message: errors.join('. '),
        type: 'danger',
        confirmText: 'OK',
        onConfirm: () => {
          // Reset file selection
          setFile(null);
          setValidationErrors([]);
        }
      });
      return;
    }
    
    // File is valid
    setValidationErrors([]);
    setIsValidFile(true);
    setFile(file);
    toast.success(`File "${file.name}" selected and ready to upload`);
  };

  const handleUpload = async () => {
    if (!file || !isValidFile) {
      toast.error("Please select a valid file first");
      return;
    }

    const form = new FormData();
    form.append("resume", file);

    setIsUploading(true);
    setUploadProgress(0);
    
    try {
      await uploadResume(form, (progress) => {
        // Update progress during upload
        setUploadProgress(Math.min(progress, 90)); // Keep some progress for processing
      });
      
      // Show processing phase
      setUploadProgress(95);
      toast.success("Resume uploaded! Processing with AI...");
      
      // Complete the progress
      setUploadProgress(100);
      setIsUploading(false);
      setUploadComplete(true);
      
      toast.success("Resume uploaded and parsed successfully!");
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
      
    } catch (error: any) {
      setIsUploading(false);
      setUploadProgress(0);
      console.error("Resume upload failed:", error);
      
      // Handle specific error cases
      const errorMessage = error.response?.data?.detail || error.message || "Failed to upload resume";
      
      if (errorMessage.includes("resume is unfit") || errorMessage.includes("not related")) {
        // Show unfit resume dialog
        setConfirmationDialog({
          isOpen: true,
          title: 'Invalid Resume',
          message: 'Resume is unfit or not related to a proper resume. Please upload a valid resume only.',
          type: 'danger',
          confirmText: 'OK',
          onConfirm: () => {
            // Reset the upload form
            resetUpload();
          }
        });
      } else if (errorMessage.includes("Unable to parse")) {
        setConfirmationDialog({
          isOpen: true,
          title: 'Unable to Parse Resume',
          message: 'Unable to parse the resume. Make sure to upload a relevant document only.',
          type: 'warning',
          confirmText: 'OK',
          onConfirm: () => {
            resetUpload();
          }
        });
      } else if (errorMessage.includes("File size") || errorMessage.includes("File type")) {
        setConfirmationDialog({
          isOpen: true,
          title: 'File Validation Error',
          message: errorMessage,
          type: 'warning',
          confirmText: 'OK',
          onConfirm: () => {
            resetUpload();
          }
        });
      } else if (error.code === 'ECONNABORTED' || errorMessage.includes('timeout')) {
        toast.error("Upload timeout. Please try again with a smaller file or check your connection.");
      } else {
        toast.error(errorMessage);
      }
    }
  };

  const resetUpload = () => {
    setFile(null);
    setUploadProgress(0);
    setUploadComplete(false);
    setIsValidFile(false);
    setValidationErrors([]);
    
    // Clear file input
    const fileInput = document.getElementById("resumeInput") as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  };

  // const doUpload = async () => {
  //   if (!file) return;
  //   const form = new FormData();
  //   /** In a real UI you‘d gather these from inputs; here we hardcode/demo */
  //   form.append("full_name", "John Doe");
  //   form.append("interested_role", "Backend Engineer");
  //   form.append("experience", "3");
  //   form.append("resume", file);

  //   setIsUploading(true);
  //   await uploadProfile(form); // ← hits /profile/
  //   setIsUploading(false);
  //   toast.success("Resume uploaded & profile saved");
  //   navigate("/dashboard");
  // };

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
            <Button variant="ghost" onClick={handleSkip} className="mt-4">Skip for now</Button>
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
                    accept=".pdf,.docx"
                    onChange={handleFileChange}
                    disabled={isUploading}
                  />
                </div>

                {file && (
                  <div className="mt-6">
                    <div className={`rounded-lg p-4 flex items-start ${
                      isValidFile 
                        ? 'bg-gray-50 dark:bg-gray-800/50' 
                        : 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
                    }`}>
                      <div className={`flex-shrink-0 p-2 rounded-full mr-4 ${
                        isValidFile 
                          ? 'bg-blue-100 dark:bg-blue-900/30' 
                          : 'bg-red-100 dark:bg-red-900/30'
                      }`}>
                        {isValidFile ? (
                          <FileText className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                        ) : (
                          <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className={`font-medium truncate ${
                          isValidFile 
                            ? 'text-gray-900 dark:text-white' 
                            : 'text-red-900 dark:text-red-100'
                        }`}>
                          {file.name}
                        </p>
                        <p className={`text-sm ${
                          isValidFile 
                            ? 'text-gray-500 dark:text-gray-400' 
                            : 'text-red-600 dark:text-red-400'
                        }`}>
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                        {!isValidFile && validationErrors.length > 0 && (
                          <div className="mt-2">
                            {validationErrors.map((error, index) => (
                              <p key={index} className="text-sm text-red-600 dark:text-red-400">
                                • {error}
                              </p>
                            ))}
                          </div>
                        )}
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
                        <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                          <span>Uploading and processing...</span>
                          <span>{uploadProgress}%</span>
                        </div>
                        <Progress value={uploadProgress} className="h-2" />
                      </div>
                    )}

                    <div className="mt-6 flex justify-end">
                      <Button 
                        onClick={handleUpload} 
                        disabled={isUploading || !isValidFile}
                        className={!isValidFile ? 'opacity-50 cursor-not-allowed' : ''}
                      >
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
                <p className="text-blue-600 dark:text-blue-400">
                  Redirecting to dashboard...
                </p>
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
                      We support PDF and DOCX formats only. For best results, make sure your resume:
                    </p>
                    <ul className="list-disc pl-5 mt-1 space-y-1">
                      <li>Is less than 1MB in size</li>
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
      
      {/* Confirmation Dialog */}
      <ConfirmationDialog
        isOpen={confirmationDialog.isOpen}
        onClose={() => setConfirmationDialog(prev => ({ ...prev, isOpen: false }))}
        onConfirm={confirmationDialog.onConfirm}
        title={confirmationDialog.title}
        message={confirmationDialog.message}
        type={confirmationDialog.type}
        confirmText={confirmationDialog.confirmText}
      />
    </div>
  );
};

export default ResumeUpload;
