<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class CoursController extends AbstractController
{
    #[Route('/cours', name: 'app_cours')]
    public function index(Request $request): Response
    {
        $section = $request->query->get('section', '');
        $valid = ['lagrange', 'newton', 'erreur', 'moindres', 'gradient'];
        if (!in_array($section, $valid)) $section = '';

        return $this->render('cours/index.html.twig', [
            'section' => $section,
        ]);
    }
}
