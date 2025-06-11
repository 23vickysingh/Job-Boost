
import React from 'react';
import { Badge } from "@/components/ui/badge";
import { X } from "lucide-react";

interface PreferencesBadgeProps {
  item: string;
  onRemove: (item: string) => void;
  variant?: "default" | "secondary" | "outline" | "destructive";
  className?: string;
}

const PreferencesBadge: React.FC<PreferencesBadgeProps> = ({ 
  item, 
  onRemove, 
  variant = "secondary",
  className = ""
}) => {
  return (
    <Badge 
      variant={variant} 
      className={`flex items-center gap-1 ${className}`}
    >
      {item}
      <button 
        onClick={() => onRemove(item)}
        className="ml-1 rounded-full hover:bg-red-200 p-0.5"
      >
        <X className="h-3 w-3" />
      </button>
    </Badge>
  );
};

export default PreferencesBadge;
