import { useEffect, useRef, useState } from 'react';
import { 
  Mountain, 
  Expand, 
  ShieldCheck, 
  MapPin, 
  Mail, 
  Phone, 
  ArrowDown,
  Trees,
  Sun,
  Home
} from 'lucide-react';
import './App.css';

function App() {
  const [isLoaded, setIsLoaded] = useState(false);
  const [scrollY, setScrollY] = useState(0);
  const heroRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setIsLoaded(true);
    
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-[#FAF9F7]">
      {/* Navigation */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrollY > 100 ? 'bg-white/95 backdrop-blur-md shadow-sm' : 'bg-transparent'
      }`}>
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            <div className={`font-display text-xl tracking-wide transition-colors duration-300 ${
              scrollY > 100 ? 'text-[#1a1a1a]' : 'text-white'
            }`}>
              4074 S 500 W
            </div>
            <div className="hidden md:flex items-center space-x-8">
              {['Features', 'Location', 'Contact'].map((item) => (
                <button
                  key={item}
                  onClick={() => scrollToSection(item.toLowerCase())}
                  className={`font-body text-xs tracking-widest uppercase transition-colors duration-300 hover:opacity-70 ${
                    scrollY > 100 ? 'text-[#1a1a1a]' : 'text-white'
                  }`}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section ref={heroRef} className="relative h-screen w-full overflow-hidden">
        {/* Background Image with Parallax */}
        <div 
          className="absolute inset-0 w-full h-full"
          style={{
            transform: `translateY(${scrollY * 0.5}px)`,
          }}
        >
          <img
            src="/hero-teton-view.jpg"
            alt="Grand Teton Mountains View"
            className="w-full h-full object-cover"
          />
        </div>
        
        {/* Gradient Overlay */}
        <div className="absolute inset-0 hero-gradient" />
        
        {/* Hero Content */}
        <div className="relative z-10 h-full flex flex-col justify-center items-center text-center px-6">
          <div className={`transition-all duration-1000 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
            <p className="font-body text-white/90 text-sm tracking-[0.3em] uppercase mb-6">
              Teton Valley, Idaho
            </p>
            <h1 className="font-display text-5xl md:text-7xl lg:text-8xl text-white mb-6 leading-tight">
              Where Majesty<br />Meets Home
            </h1>
            <div className="section-divider mb-8 bg-white/60" />
            <p className="font-body text-white/80 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
              Unobstructed views of the Grand Teton peaks from your window.<br />
              A half-acre of freedom with no restrictions.
            </p>
          </div>
          
          {/* Scroll Indicator */}
          <button 
            onClick={() => scrollToSection('features')}
            className={`absolute bottom-12 left-1/2 -translate-x-1/2 text-white/70 hover:text-white transition-all duration-500 animate-bounce ${
              isLoaded ? 'opacity-100' : 'opacity-0'
            }`}
            style={{ animationDelay: '1s' }}
          >
            <ArrowDown className="w-6 h-6" />
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 lg:py-32 bg-[#FAF9F7]">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          {/* Section Header */}
          <div className="text-center mb-20">
            <p className="font-body text-[#8B6914] text-sm tracking-[0.25em] uppercase mb-4">
              Property Highlights
            </p>
            <h2 className="font-display text-4xl md:text-5xl lg:text-6xl text-[#1a1a1a] mb-6">
              Your Private Sanctuary
            </h2>
            <div className="section-divider" />
          </div>

          {/* Feature Cards */}
          <div className="grid md:grid-cols-3 gap-8 lg:gap-12">
            {/* Feature 1 - Unobstructed Views */}
            <div className="feature-card bg-white rounded-sm p-8 lg:p-10 shadow-sm">
              <div className="w-14 h-14 bg-[#F5F0E8] rounded-full flex items-center justify-center mb-6">
                <Mountain className="w-7 h-7 text-[#8B6914]" />
              </div>
              <h3 className="font-display text-2xl text-[#1a1a1a] mb-4">
                Unobstructed Teton Views
              </h3>
              <p className="font-body text-[#5a5a5a] leading-relaxed">
                Direct views of the majestic Grand Teton peaks from your front window. 
                With no possibility of future building or blocked views, this panorama 
                is yours to keep forever.
              </p>
            </div>

            {/* Feature 2 - Half Acre */}
            <div className="feature-card bg-white rounded-sm p-8 lg:p-10 shadow-sm">
              <div className="w-14 h-14 bg-[#F5F0E8] rounded-full flex items-center justify-center mb-6">
                <Expand className="w-7 h-7 text-[#8B6914]" />
              </div>
              <h3 className="font-display text-2xl text-[#1a1a1a] mb-4">
                Spacious Half Acre
              </h3>
              <p className="font-body text-[#5a5a5a] leading-relaxed">
                Room to breathe, expand, and create. With half an acre of land, 
                you have the space to build additional structures, create gardens, 
                or simply enjoy the open Idaho sky.
              </p>
            </div>

            {/* Feature 3 - No C&Rs */}
            <div className="feature-card bg-white rounded-sm p-8 lg:p-10 shadow-sm">
              <div className="w-14 h-14 bg-[#F5F0E8] rounded-full flex items-center justify-center mb-6">
                <ShieldCheck className="w-7 h-7 text-[#8B6914]" />
              </div>
              <h3 className="font-display text-2xl text-[#1a1a1a] mb-4">
                No Covenants or Restrictions
              </h3>
              <p className="font-body text-[#5a5a5a] leading-relaxed">
                Complete freedom to build, modify, and use your property as you see fit. 
                No HOA fees, no restrictive covenants — just pure ownership autonomy 
                in the heart of Teton Valley.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Visual Showcase Section */}
      <section className="py-0">
        <div className="grid lg:grid-cols-2">
          {/* Image 1 */}
          <div className="img-zoom relative h-[500px] lg:h-[700px]">
            <img
              src="/property-aerial.jpg"
              alt="Aerial view of property with Teton mountains"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
            <div className="absolute bottom-8 left-8 right-8">
              <p className="font-body text-white/80 text-sm tracking-widest uppercase mb-2">
                Your View
              </p>
              <h3 className="font-display text-3xl text-white">
                Endless Horizons
              </h3>
            </div>
          </div>

          {/* Image 2 */}
          <div className="img-zoom relative h-[500px] lg:h-[700px]">
            <img
              src="/interior-view.jpg"
              alt="Interior view looking out at Tetons"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
            <div className="absolute bottom-8 left-8 right-8">
              <p className="font-body text-white/80 text-sm tracking-widest uppercase mb-2">
                Your Home
              </p>
              <h3 className="font-display text-3xl text-white">
                Mountain Living
              </h3>
            </div>
          </div>
        </div>
      </section>

      {/* Location Section */}
      <section id="location" className="py-24 lg:py-32 bg-white">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* Content */}
            <div>
              <p className="font-body text-[#8B6914] text-sm tracking-[0.25em] uppercase mb-4">
                The Location
              </p>
              <h2 className="font-display text-4xl md:text-5xl text-[#1a1a1a] mb-6">
                Teton Valley, Idaho
              </h2>
              <div className="w-16 h-px bg-[#8B6914] mb-8" />
              
              <p className="font-body text-[#5a5a5a] leading-relaxed mb-8">
                Known as the "quiet side of the Grand Tetons," Teton Valley offers 
                a serene escape from the crowds while keeping you connected to world-class 
                outdoor recreation. The west-facing views from Victor are often considered 
                the most spectacular in the region.
              </p>

              {/* Location Features */}
              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-[#F5F0E8] rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <MapPin className="w-5 h-5 text-[#8B6914]" />
                  </div>
                  <div>
                    <h4 className="font-display text-lg text-[#1a1a1a] mb-1">
                      4074 S 500 W, Victor, ID
                    </h4>
                    <p className="font-body text-[#5a5a5a] text-sm">
                      Perfectly positioned in the heart of Teton Valley
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-[#F5F0E8] rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <Trees className="w-5 h-5 text-[#8B6914]" />
                  </div>
                  <div>
                    <h4 className="font-display text-lg text-[#1a1a1a] mb-1">
                      Outdoor Paradise
                    </h4>
                    <p className="font-body text-[#5a5a5a] text-sm">
                      Minutes from Grand Targhee Resort, world-class fishing, and endless trails
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-[#F5F0E8] rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <Sun className="w-5 h-5 text-[#8B6914]" />
                  </div>
                  <div>
                    <h4 className="font-display text-lg text-[#1a1a1a] mb-1">
                      Four-Season Beauty
                    </h4>
                    <p className="font-body text-[#5a5a5a] text-sm">
                      From wildflower summers to powder snow winters, experience it all
                    </p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-[#F5F0E8] rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <Home className="w-5 h-5 text-[#8B6914]" />
                  </div>
                  <div>
                    <h4 className="font-display text-lg text-[#1a1a1a] mb-1">
                      Small Town Charm
                    </h4>
                    <p className="font-body text-[#5a5a5a] text-sm">
                      Close to Victor and Driggs amenities, farmers markets, and local dining
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="bg-[#FAF9F7] rounded-sm p-10 lg:p-12">
              <h3 className="font-display text-2xl text-[#1a1a1a] mb-8 text-center">
                At a Glance
              </h3>
              
              <div className="grid grid-cols-2 gap-8">
                <div className="text-center">
                  <p className="font-display text-4xl lg:text-5xl text-[#8B6914] mb-2">
                    0.5
                  </p>
                  <p className="font-body text-[#5a5a5a] text-sm tracking-widest uppercase">
                    Acres
                  </p>
                </div>
                
                <div className="text-center">
                  <p className="font-display text-4xl lg:text-5xl text-[#8B6914] mb-2">
                    13,775
                  </p>
                  <p className="font-body text-[#5a5a5a] text-sm tracking-widest uppercase">
                    Ft — Grand Teton
                  </p>
                </div>
                
                <div className="text-center">
                  <p className="font-display text-4xl lg:text-5xl text-[#8B6914] mb-2">
                    0
                  </p>
                  <p className="font-body text-[#5a5a5a] text-sm tracking-widest uppercase">
                    C&Rs
                  </p>
                </div>
                
                <div className="text-center">
                  <p className="font-display text-4xl lg:text-5xl text-[#8B6914] mb-2">
                    ∞
                  </p>
                  <p className="font-body text-[#5a5a5a] text-sm tracking-widest uppercase">
                    Possibilities
                  </p>
                </div>
              </div>

              <div className="mt-10 pt-8 border-t border-[#E5E0D8]">
                <p className="font-body text-[#5a5a5a] text-center text-sm leading-relaxed">
                  Grand Teton National Park is just a short drive away, offering 
                  242 miles of trails, pristine lakes, and some of the most 
                  spectacular mountain scenery in North America.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="relative py-24 lg:py-32">
        {/* Background */}
        <div className="absolute inset-0">
          <img
            src="/hero-teton-view.jpg"
            alt="Teton mountains"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-[#1a1a1a]/80" />
        </div>

        {/* Content */}
        <div className="relative z-10 max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <p className="font-body text-[#8B6914] text-sm tracking-[0.25em] uppercase mb-4">
            Get in Touch
          </p>
          <h2 className="font-display text-4xl md:text-5xl lg:text-6xl text-white mb-6">
            Make This View Yours
          </h2>
          <div className="section-divider mb-10 bg-white/30" />
          
          <p className="font-body text-white/80 text-lg leading-relaxed max-w-2xl mx-auto mb-12">
            Opportunities like this are rare. A home with unobstructed Teton views, 
            half an acre of land, and complete freedom to create your mountain sanctuary. 
            Contact Brian Clark to schedule a viewing.
          </p>

          {/* Contact Cards */}
          <div className="grid md:grid-cols-2 gap-6 max-w-2xl mx-auto">
            <a 
              href="mailto:blclark4074@gmail.com"
              className="group bg-white/10 backdrop-blur-sm rounded-sm p-8 hover:bg-white/20 transition-all duration-300"
            >
              <Mail className="w-8 h-8 text-[#8B6914] mx-auto mb-4 group-hover:scale-110 transition-transform" />
              <p className="font-body text-white/60 text-xs tracking-widest uppercase mb-2">
                Email
              </p>
              <p className="font-body text-white">
                blclark4074@gmail.com
              </p>
            </a>

            <a 
              href="tel:9864978425"
              className="group bg-white/10 backdrop-blur-sm rounded-sm p-8 hover:bg-white/20 transition-all duration-300"
            >
              <Phone className="w-8 h-8 text-[#8B6914] mx-auto mb-4 group-hover:scale-110 transition-transform" />
              <p className="font-body text-white/60 text-xs tracking-widest uppercase mb-2">
                Phone
              </p>
              <p className="font-body text-white">
                (986) 497-8425
              </p>
            </a>
          </div>

          {/* Agent Info */}
          <div className="mt-12 pt-8 border-t border-white/20">
            <p className="font-display text-2xl text-white mb-2">
              Brian Clark
            </p>
            <p className="font-body text-white/60 text-sm">
              4074 S 500 W, Victor, Idaho
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#1a1a1a] py-8">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
            <p className="font-display text-white/80 text-lg">
              4074 S 500 W
            </p>
            <p className="font-body text-white/40 text-sm">
              Teton Valley, Idaho — For Sale by Owner
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
