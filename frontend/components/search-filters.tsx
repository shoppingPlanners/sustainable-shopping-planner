"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search, Filter, SortAsc } from "lucide-react";
import { useSearchTracking } from "@/hooks/use-tracking";
import { useState, useCallback } from "react";

interface SearchFiltersProps {
  onSearch?: (query: string, filters: Record<string, any>) => void;
  onFilterChange?: (filterType: string, value: string) => void;
  categories?: string[];
  priceRanges?: string[];
  page?: string;
}

export function SearchFilters({ 
  onSearch, 
  onFilterChange, 
  categories = ["all", "dresses", "tops", "t-shirts", "summer"],
  priceRanges = ["all", "under-20", "20-30", "30-50", "50-plus"],
  page = "/suggestions"
}: SearchFiltersProps) {
  const { handleSearch, handleFilterChange } = useSearchTracking();
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [selectedPriceRange, setSelectedPriceRange] = useState("all");
  const [selectedSort, setSelectedSort] = useState("relevance");

  const handleSearchSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      const filters = {
        category: selectedCategory,
        priceRange: selectedPriceRange,
        sort: selectedSort,
      };
      
      handleSearch(searchQuery.trim(), filters);
      onSearch?.(searchQuery.trim(), filters);
    }
  }, [searchQuery, selectedCategory, selectedPriceRange, selectedSort, handleSearch, onSearch]);

  const handleCategoryChange = useCallback((value: string) => {
    setSelectedCategory(value);
    handleFilterChange("category", value);
    onFilterChange?.("category", value);
  }, [handleFilterChange, onFilterChange]);

  const handlePriceRangeChange = useCallback((value: string) => {
    setSelectedPriceRange(value);
    handleFilterChange("price_range", value);
    onFilterChange?.("price_range", value);
  }, [handleFilterChange, onFilterChange]);

  const handleSortChange = useCallback((value: string) => {
    setSelectedSort(value);
    handleFilterChange("sort", value);
    onFilterChange?.("sort", value);
  }, [handleFilterChange, onFilterChange]);

  const handleSearchInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  }, []);

  const handleSearchBlur = useCallback(() => {
    if (searchQuery.trim()) {
      const keywords = searchQuery.trim().split(/\s+/);
      handleSearch(keywords.join(" "), {
        category: selectedCategory,
        priceRange: selectedPriceRange,
        sort: selectedSort,
      });
    }
  }, [searchQuery, selectedCategory, selectedPriceRange, selectedSort, handleSearch]);

  return (
    <div className="flex flex-col sm:flex-row gap-4 items-center justify-between bg-card rounded-lg p-4 border border-border">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Filter className="h-4 w-4" />
        <span>Filter:</span>
      </div>

      <div className="flex flex-col sm:flex-row gap-3 w-full sm:w-auto">
        {/* Search Input */}
        <form onSubmit={handleSearchSubmit} className="relative w-full sm:w-[200px]">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Search products..." 
            className="pl-9"
            value={searchQuery}
            onChange={handleSearchInputChange}
            onBlur={handleSearchBlur}
          />
        </form>

        {/* Category Filter */}
        <Select value={selectedCategory} onValueChange={handleCategoryChange}>
          <SelectTrigger className="w-full sm:w-[140px]">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            {categories.map((category) => (
              <SelectItem key={category} value={category}>
                {category === "all" ? "All Items" : 
                 category === "dresses" ? "Dresses" :
                 category === "tops" ? "Tops & Blouses" :
                 category === "t-shirts" ? "T-shirts" :
                 category === "summer" ? "Summer Collection" : category}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Price Range Filter */}
        <Select value={selectedPriceRange} onValueChange={handlePriceRangeChange}>
          <SelectTrigger className="w-full sm:w-[140px]">
            <SelectValue placeholder="Price Range" />
          </SelectTrigger>
          <SelectContent>
            {priceRanges.map((range) => (
              <SelectItem key={range} value={range}>
                {range === "all" ? "All Prices" : 
                 range === "under-20" ? "Under $20" :
                 range === "20-30" ? "$20 - $30" :
                 range === "30-50" ? "$30 - $50" :
                 range === "50-plus" ? "$50+" : range}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Sort Filter */}
        <Select value={selectedSort} onValueChange={handleSortChange}>
          <SelectTrigger className="w-full sm:w-[140px]">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="relevance">Relevance</SelectItem>
            <SelectItem value="price-low">Price: Low to High</SelectItem>
            <SelectItem value="price-high">Price: High to Low</SelectItem>
            <SelectItem value="rating">Rating</SelectItem>
            <SelectItem value="sustainability">Sustainability</SelectItem>
            <SelectItem value="newest">Newest</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}
