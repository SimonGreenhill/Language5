from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from website.apps.lexicon.models import Lexicon
from website.apps.pronouns.tools import full_repr_row
from website.apps.pronouns.models import Paradigm, PronounType, Pronoun, Relationship
from website.apps.pronouns.tests import PronounsTestData

from website.apps.core.tests.utils import PaginatorTestMixin

class Test_Index(PronounsTestData, PaginatorTestMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        super(Test_Index, cls).setUpTestData()
        cls.url = reverse('pronouns:index')
        cls.client = Client()
        cls.response = cls.client.get(cls.url)
    
    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'pronouns/index.html')
    
    def test_shows_paradigms(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Smith (1991)')
    
    def test_shows_labels(self):
        p = self.pdm
        p.label = 'sausage'
        p.pk = None
        p.save()
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, unicode(p))
        self.assertContains(self.response, 'sausage')
        

class Test_Detail(PronounsTestData, TestCase):
    @classmethod
    def setUpTestData(cls):
        super(Test_Detail, cls).setUpTestData()
        self.url = reverse('pronouns:detail', kwargs={'paradigm_id': self.pdm.id})
        self.client = Client()
        self.response = self.client.get(self.url)

    def test_200ok(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'pronouns/detail.html')

    def test_language_in_content(self):
        self.assertContains(self.response, '/language/langa')

    def test_comment_in_content(self):
        self.assertContains(self.response, 'test')

    def test_label_in_content(self):
        assert False
        # self.pdm.label = 'sausage'
        # self.pdm.save()
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, unicode(self.pdm))
        self.assertContains(self.response, 'sausage')
        self.assertContains(
            self.response, '<h1>Pronoun Paradigm: A: sausage</h1>'
        )

    def test_content_rows(self):
        for p in self.pdm.pronoun_set.all():
            self.assertContains(self.response, full_repr_row(p))

    def test_content_values(self):
        for p in self.pdm.pronoun_set.all():
            self.assertContains(self.response, p.entries.all()[0].entry)

    def test_content_multiple_values(self):
        assert False
        for counter, p in enumerate(self.pdm.pronoun_set.all(), 1):
            lex = Lexicon.objects.create(
                editor=self.editor,
                language=self.lang,
                source=self.source,
                word=self.word,
                entry='cake-%d' % counter
            )
            lex.save()
            p.entries.add(lex)

        response = self.client.get(self.url)
        for p in self.pdm.pronoun_set.all():
            for e in p.entries.all():
                self.assertContains(response, e.entry)

    def test_shows_relationships(self):
        """Should show defined relationships if present"""
        assert False
        self._create_relationship()
        assert self.pdm.relationship_set.count() == 1, \
            "I was expecting one relationship to be defined!"

        # re-call the view.
        response = self.client.get(self.url)

        # test
        assert response.context['relationship_table'] is not None, \
            "Template variable relationship_table should be initialised"
        self.assertContains(response, "Relationships")

    def test_hides_relationships(self):
        """Should NOT show relationships block if none are given"""
        assert self.pdm.relationship_set.count() == 0, \
            "I was expecting NO relationships to be defined!"
        self.assertNotContains(self.response, "Relationships")

    def test_relationship_details(self):
        assert False
        rel = self._create_relationship()
        assert self.pdm.relationship_set.count() == 1, \
            "I was expecting one relationship to be defined!"

        # re-call the view.
        response = self.client.get(self.url)
        self.assertContains(response, "fudge-%d" % rel.pronoun1.id)
        self.assertContains(response, "fudge-%d" % rel.pronoun2.id)



# Test View: Add paradigm
class Test_AddParadigmView(PronounsTestData, TestCase):
    @classmethod
    def setUpTestData(cls):
        super(Test_AddParadigmView, cls).setUpTestData()
        cls.url = reverse('pronouns:add')
    
    def setUp(self):
        self.client = Client()
        self.client.login(username='admin', password='test')

    def test_200ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'pronouns/add.html')

    def test_fail_when_not_logged_in(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "%s?next=%s" % (reverse('login'), reverse("pronouns:add"))
        )

    def test_paradigm_save(self):
        count = Paradigm.objects.count()
        self.client.login(username='admin', password='test')
        response = self.client.post(self.url, {
            'language': self.lang.id,
            'source': self.source.id,
            'comment': 'French'
        }, follow=True)
        self.assertEqual(Paradigm.objects.count(), count + 1)
        self.assertContains(response, 'French')

    def test_paradigm_creates_pronouns(self):
        count = Pronoun.objects.count()
        self.client.post(self.url, {
            'language': self.lang.id,
            'source': self.source.id,
            'comment': ''
        }, follow=True)
        self.assertEqual(
            Pronoun.objects.count(),
            count + len(PronounType._generate_all_combinations())
        )

    def test_paradigm_save_with_label(self):
        count = Paradigm.objects.count()
        response = self.client.post(self.url, {
            'language': self.lang.id,
            'source': self.source.id,
            'comment': 'foo',
            'label': 'Xyzzy'
        }, follow=True)
        self.assertEqual(Paradigm.objects.count(), count + 1)
        self.assertContains(response, 'Xyzzy')
