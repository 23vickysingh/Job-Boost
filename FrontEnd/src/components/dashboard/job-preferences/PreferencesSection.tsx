
import React from 'react';
import { Label } from "@/components/ui/label";
import PreferencesBadge from './PreferencesBadge';
import AddItemInput from './AddItemInput';

interface PreferencesSectionProps {
  title: string;
  items: string[];
  onRemove: (item: string) => void;
  onAdd: (item: string) => void;
  placeholder: string;
  badgeVariant?: "default" | "secondary" | "outline" | "destructive";
  badgeClassName?: string;
}

const PreferencesSection: React.FC<PreferencesSectionProps> = ({
  title,
  items,
  onRemove,
  onAdd,
  placeholder,
  badgeVariant = "secondary",
  badgeClassName = ""
}) => {
  return (
    <div>
      <Label>{title}</Label>
      <div className="flex flex-wrap gap-2 mt-2 mb-2">
        {items.map((item, index) => (
          <PreferencesBadge 
            key={index} 
            item={item} 
            onRemove={onRemove} 
            variant={badgeVariant}
            className={badgeClassName}
          />
        ))}
      </div>
      <AddItemInput 
        placeholder={placeholder} 
        onAdd={onAdd} 
      />
    </div>
  );
};

export default PreferencesSection;
