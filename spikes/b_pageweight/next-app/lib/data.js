// Mock data shaped like the Mek Academy demo: 12 courses, 8 lessons each, English and Amharic text.
const topics = ['Excel for the Workplace', 'Project Management Fundamentals', 'Business Writing', 'Bookkeeping Basics', 'Customer Service',
  'Digital Marketing', 'Leadership Essentials', 'Public Speaking', 'Data Analysis', 'Entrepreneurship', 'Time Management', 'Negotiation Skills'];
const levels = ['Beginner', 'Intermediate', 'Advanced'];
const para = 'Practical, professional training taught by experienced teachers. Watch lessons, download materials, test yourself and earn a certificate on your phone or computer. ';
const amPara = 'ተግባራዊ እና ሙያዊ ሥልጠና በልምድ ባላቸው መምህራን። ትምህርቶችን ይመልከቱ፣ ቁሳቁሶችን ያውርዱ፣ ራስዎን ይፈትኑ እና በስልክዎ ወይም በኮምፒውተርዎ ሰርተፍኬት ያግኙ። ';
export const courses = topics.map((title, i) => ({
  slug: title.toLowerCase().replace(/[^a-z]+/g, '-'),
  title, level: levels[i % 3], hours: 6 + (i % 5) * 3, price: i % 4 === 0 ? 0 : 1500 + i * 250,
  summary: 'Plan, run and finish work on time using proven tools and templates.',
  rating: (4 + (i % 10) / 10).toFixed(1), reviews: 20 + i * 7,
  lessons: Array.from({ length: 8 }, (_, j) => ({ id: i * 10 + j + 1, title: `Lesson ${j + 1}: ${title.split(' ')[0]} in practice`, minutes: 8 + j * 2, preview: j === 0 })),
}));
export const lessonBody = (n) => Array.from({ length: n }, () => para + amPara);
export const allLessons = courses.flatMap((c) => c.lessons.map((l) => ({ ...l, course: c })));
